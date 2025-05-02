const axios = require('axios');
const path = require('path');
const fs = require('fs-extra');
const config = require('../config');

class FileSync {
  constructor() {
    this.config = config;
    this.axios = axios.create({
      baseURL: this.config.apiEndpoint,
      headers: {
        'Authorization': `Bearer ${this.config.apiToken}`,
        'Content-Type': 'application/json'
      },
      timeout: 10000,
      maxBodyLength: 100 * 1024 * 1024, // 100MB 限制
      maxContentLength: 100 * 1024 * 1024
    });
  }

  /**
   * 发送文件内容到服务器
   * @param {string} filePath - 文件路径
   * @param {string} action - 操作类型 (add, change, delete)
   * @returns {Promise<Object>} - 服务器响应
   */
  async syncFile(filePath, action) {
    const relativePath = path.relative(this.config.watchDir, filePath);
    let content = null;
    let is_binary = false;
    let retries = 0;
    
    if (action !== 'delete') {
      try {
        // 判断文件类型
        is_binary = this.isBinaryFile(filePath);
        
        if (is_binary) {
          // 读取二进制文件并转为base64
          const buffer = await fs.readFile(filePath);
          content = buffer.toString('base64');
          this.logDebug(`读取二进制文件: ${filePath} (${buffer.length} 字节)`);
        } else {
          // 读取文本文件
          content = await fs.readFile(filePath, 'utf8');
          this.logDebug(`读取文本文件: ${filePath} (${content.length} 字符)`);
        }
      } catch (error) {
        this.logDebug(`读取文件失败: ${filePath}`, error);
        throw new Error(`无法读取文件: ${error.message}`);
      }
    }

    const payload = {
      action,
      path: relativePath,
      content,
      is_binary,
      timestamp: new Date().toISOString()
    };

    while (retries < this.config.retryCount) {
      try {
        this.logDebug(`尝试同步文件 ${filePath} - 操作: ${action} - 二进制: ${is_binary}`);
        const response = await this.axios.post('/sync', payload);
        this.logDebug(`同步成功: ${filePath}`);
        return response.data;
      } catch (error) {
        retries++;
        this.logDebug(`同步失败 (尝试 ${retries}/${this.config.retryCount}): ${filePath}`, error);
        
        if (retries >= this.config.retryCount) {
          throw new Error(`同步失败，已达最大重试次数: ${error.message}`);
        }
        
        // 等待重试
        await new Promise(resolve => setTimeout(resolve, this.config.retryInterval));
      }
    }
  }

  /**
   * 判断是否为二进制文件
   * @param {string} filePath - 文件路径
   * @returns {boolean} - 是否为二进制文件
   */
  isBinaryFile(filePath) {
    // 根据文件扩展名判断
    const ext = path.extname(filePath).toLowerCase();
    
    // 常见文本文件扩展名
    const textExtensions = [
      '.md', '.txt', '.json', '.js', '.ts', '.html', '.css', '.scss', '.less',
      '.xml', '.svg', '.yml', '.yaml', '.ini', '.conf', '.sh', '.bat',
      '.c', '.cpp', '.h', '.java', '.py', '.rb', '.php', '.go', '.cs',
      '.jsx', '.tsx', '.vue', '.csv', '.log'
    ];
    
    // 常见二进制文件扩展名
    const binaryExtensions = [
      '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp',
      '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
      '.zip', '.rar', '.7z', '.tar', '.gz', '.mp3', '.mp4', '.avi',
      '.mov', '.wmv', '.wav', '.flac', '.exe', '.dll', '.so', '.bin'
    ];
    
    if (textExtensions.includes(ext)) {
      return false;
    }
    
    if (binaryExtensions.includes(ext)) {
      return true;
    }
    
    // 对于未知扩展名，尝试读取文件头部内容进行判断
    try {
      // 读取文件前1024个字节
      const buffer = Buffer.alloc(1024);
      const fd = fs.openSync(filePath, 'r');
      const bytesRead = fs.readSync(fd, buffer, 0, 1024, 0);
      fs.closeSync(fd);
      
      // 检查是否包含空字节（通常表示二进制文件）
      for (let i = 0; i < bytesRead; i++) {
        if (buffer[i] === 0) {
          return true;
        }
      }
      
      // 如果文件很大（>1MB），也认为是二进制文件
      const stats = fs.statSync(filePath);
      if (stats.size > 1024 * 1024) {
        return true;
      }
      
      // 默认当作文本文件
      return false;
    } catch (error) {
      this.logDebug(`检查文件类型错误: ${filePath}`, error);
      return false;
    }
  }

  /**
   * 输出调试信息
   * @param {string} message - 消息内容
   * @param {Error} [error] - 错误对象
   */
  logDebug(message, error = null) {
    if (this.config.debug) {
      console.log(`[${new Date().toISOString()}] ${message}`);
      if (error) {
        console.error(error.stack || error);
      }
    }
  }
}

module.exports = new FileSync(); 