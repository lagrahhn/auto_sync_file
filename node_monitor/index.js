const watcher = require('./utils/watcher');
const config = require('./config');
const fs = require('fs-extra');
const path = require('path');

/**
 * 应用程序主入口
 */
async function main() {
  try {
    console.log('=== Markdown 自动同步服务 ===');
    console.log(`版本: 1.0.0`);
    console.log(`调试模式: ${config.debug ? '开启' : '关闭'}`);
    
    // 确保监控目录存在
    await fs.ensureDir(config.watchDir);
    console.log(`监控目录: ${config.watchDir}`);
    
    // 启动文件监控
    await watcher.start();
  } catch (error) {
    console.error('启动失败:', error);
    process.exit(1);
  }
}

/**
 * 优雅退出处理
 */
async function gracefulShutdown() {
  console.log('正在关闭应用...');
  
  try {
    await watcher.stop();
    console.log('应用已安全关闭');
    process.exit(0);
  } catch (error) {
    console.error('关闭时发生错误:', error);
    process.exit(1);
  }
}

// 注册退出信号处理
process.on('SIGINT', gracefulShutdown);
process.on('SIGTERM', gracefulShutdown);
process.on('SIGHUP', gracefulShutdown);

// 未捕获异常处理
process.on('uncaughtException', (error) => {
  console.error('未捕获异常:', error);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('未处理的Promise拒绝:', reason);
});

// 启动应用
main(); 