#!/usr/bin/env node

const fs = require('fs-extra');
const path = require('path');
const { exec } = require('child_process');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

/**
 * 执行命令
 * @param {string} command - 要执行的命令
 * @returns {Promise<string>} - 命令输出
 */
function executeCommand(command) {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`执行命令失败: ${error.message}`);
        reject(error);
        return;
      }
      resolve(stdout.trim());
    });
  });
}

/**
 * 询问用户
 * @param {string} question - 问题
 * @returns {Promise<string>} - 用户回答
 */
function askQuestion(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

/**
 * 主安装流程
 */
async function install() {
  console.log('=== Markdown自动同步工具安装 ===');
  console.log('此脚本将帮助您完成安装和初始配置。\n');
  
  try {
    // 安装依赖
    console.log('正在安装依赖...');
    await executeCommand('npm install');
    console.log('依赖安装完成。\n');
    
    // 创建配置
    const createConfig = await askQuestion('是否要创建自定义配置文件? (y/n): ');
    
    if (createConfig.toLowerCase() === 'y') {
      const watchDir = await askQuestion('请输入要监控的文件夹路径 (默认: ./markdown): ');
      const apiEndpoint = await askQuestion('请输入服务器API地址: ');
      const apiToken = await askQuestion('请输入API认证令牌: ');
      const debug = await askQuestion('是否开启调试模式? (y/n): ');
      
      // 创建配置文件
      const configContent = `
const path = require('path');

module.exports = {
  watchDir: ${watchDir ? `path.resolve(__dirname, '${watchDir}')` : 'path.resolve(__dirname, "markdown")'},
  apiEndpoint: '${apiEndpoint || 'http://example.com/api/sync'}',
  apiToken: '${apiToken || 'your_api_token'}',
  debug: ${debug.toLowerCase() === 'y' ? 'true' : 'false'}
};`;

      await fs.writeFile(path.join(__dirname, 'config.local.js'), configContent);
      console.log('自定义配置文件已创建: config.local.js\n');
      
      // 创建监控目录
      const dirToCreate = watchDir || 'markdown';
      await fs.ensureDir(path.join(__dirname, dirToCreate));
      console.log(`监控目录已创建: ${dirToCreate}\n`);
    }
    
    // PM2安装
    const installPM2 = await askQuestion('是否要安装PM2用于进程守护和开机自启? (y/n): ');
    
    if (installPM2.toLowerCase() === 'y') {
      console.log('正在安装PM2...');
      await executeCommand('npm install pm2 -g');
      console.log('PM2安装完成。\n');
      
      console.log('配置开机自启动...');
      await executeCommand('pm2 start ecosystem.config.js');
      await executeCommand('pm2 save');
      
      // 尝试配置开机自启
      try {
        await executeCommand('pm2 startup');
        console.log('请根据上面的提示，执行相应的命令以启用开机自启。\n');
      } catch (e) {
        console.log('无法自动配置开机自启，请手动配置。\n');
      }
    }
    
    console.log('=== 安装完成 ===');
    console.log('您可以通过以下命令启动服务:');
    console.log('- 普通启动: npm start');
    console.log('- 开发模式: npm run dev');
    console.log('- PM2守护进程: pm2 start ecosystem.config.js');
  } catch (error) {
    console.error('安装过程中发生错误:', error);
  } finally {
    rl.close();
  }
}

// 开始安装
install(); 