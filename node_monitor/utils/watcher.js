const chokidar = require('chokidar');
const path = require('path');
const fs = require('fs-extra');
const config = require('../config');
const fileSync = require('./fileSync');

class Watcher {
  constructor() {
    this.config = config;
    this.watcher = null;
    this.isReady = false;
  }

  /**
   * 启动文件监控
   */
  async start() {
    // 确保监控目录存在
    await fs.ensureDir(this.config.watchDir);
    
    console.log(`开始监控目录: ${this.config.watchDir}`);
    
    // 初始化监控器
    this.watcher = chokidar.watch(this.config.watchDir, {
      ignored: this.config.ignorePatterns,
      ignoreInitial: false,
      persistent: true,
      awaitWriteFinish: {
        stabilityThreshold: 2000,
        pollInterval: 100
      }
    });

    // 添加事件监听
    this.watcher
      .on('add', filePath => this.handleFileAdded(filePath))
      .on('change', filePath => this.handleFileChanged(filePath))
      .on('unlink', filePath => this.handleFileDeleted(filePath))
      .on('ready', () => this.handleWatcherReady())
      .on('error', error => this.handleError(error));
      
    return this.watcher;
  }

  /**
   * 停止文件监控
   */
  async stop() {
    if (this.watcher) {
      console.log('停止文件监控...');
      await this.watcher.close();
      this.watcher = null;
      this.isReady = false;
      console.log('文件监控已停止');
    }
  }

  /**
   * 处理文件添加事件
   * @param {string} filePath - 文件路径
   */
  async handleFileAdded(filePath) {
    if (!this.shouldProcessFile(filePath)) return;
    
    try {
      // 只有在监控器准备好后才处理初始文件
      if (this.isReady) {
        console.log(`检测到新文件: ${filePath}`);
        await fileSync.syncFile(filePath, 'add');
      }
    } catch (error) {
      console.error(`处理新文件失败: ${filePath}`, error);
    }
  }

  /**
   * 处理文件变更事件
   * @param {string} filePath - 文件路径
   */
  async handleFileChanged(filePath) {
    if (!this.shouldProcessFile(filePath)) return;
    
    try {
      console.log(`检测到文件变更: ${filePath}`);
      await fileSync.syncFile(filePath, 'change');
    } catch (error) {
      console.error(`处理文件变更失败: ${filePath}`, error);
    }
  }

  /**
   * 处理文件删除事件
   * @param {string} filePath - 文件路径
   */
  async handleFileDeleted(filePath) {
    if (!this.shouldProcessFile(filePath)) return;
    
    try {
      console.log(`检测到文件删除: ${filePath}`);
      await fileSync.syncFile(filePath, 'delete');
    } catch (error) {
      console.error(`处理文件删除失败: ${filePath}`, error);
    }
  }

  /**
   * 处理监控器就绪事件
   */
  handleWatcherReady() {
    this.isReady = true;
    console.log('文件监控已就绪，正在监控变更...');
  }

  /**
   * 处理监控器错误
   * @param {Error} error - 错误对象
   */
  handleError(error) {
    console.error('监控器发生错误:', error);
  }

  /**
   * 判断文件是否应该被处理
   * @param {string} filePath - 文件路径
   * @returns {boolean} - 是否应该处理此文件
   */
  shouldProcessFile(filePath) {
    // 如果配置了只监控特定类型的文件
    if (this.config.fileTypes && this.config.fileTypes.length > 0) {
      const ext = path.extname(filePath).toLowerCase();
      return this.config.fileTypes.includes(ext);
    }
    
    // 如果配置了排除特定类型的文件
    if (this.config.excludeFileTypes && this.config.excludeFileTypes.length > 0) {
      const ext = path.extname(filePath).toLowerCase();
      return !this.config.excludeFileTypes.includes(ext);
    }
    
    // 默认处理所有文件
    return true;
  }

  /**
   * 检查文件是否为Markdown文件 (保留以兼容旧代码)
   * @param {string} filePath - 文件路径
   * @returns {boolean} - 是否为Markdown文件
   */
  isMarkdownFile(filePath) {
    return path.extname(filePath).toLowerCase() === '.md';
  }
}

module.exports = new Watcher(); 