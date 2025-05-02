/**
 * Windows服务安装脚本
 * 
 * 此脚本用于将应用安装为Windows服务
 * 需要先全局安装node-windows包：npm install -g node-windows
 */

const Service = require('node-windows').Service;
const path = require('path');
const fs = require('fs-extra');

// 创建一个新的服务对象
const svc = new Service({
  name: 'MarkdownSync',
  description: 'Markdown文件自动同步服务',
  script: path.join(__dirname, 'index.js'),
  nodeOptions: [],
  workingDirectory: __dirname,
  allowServiceLogon: true
});

// 监听安装事件
svc.on('install', function() {
  console.log('服务已成功安装');
  svc.start();
  console.log('服务已启动');
});

// 监听启动事件
svc.on('start', function() {
  console.log('服务已启动');
});

// 监听卸载事件
svc.on('uninstall', function() {
  console.log('服务已成功卸载');
});

// 监听错误事件
svc.on('error', function(err) {
  console.error('服务错误:', err);
});

// 检查命令行参数，决定安装还是卸载
const args = process.argv.slice(2);
if (args.includes('--uninstall')) {
  console.log('正在卸载Windows服务...');
  svc.uninstall();
} else {
  console.log('正在安装Windows服务...');
  
  // 确保node-windows已安装
  try {
    require.resolve('node-windows');
  } catch (e) {
    console.log('未找到node-windows模块，正在安装...');
    require('child_process').execSync('npm install node-windows --save');
    console.log('node-windows已安装');
  }
  
  // 安装服务
  svc.install();
}

/**
 * 使用方法：
 * 
 * 1. 安装服务：node windows-service.js
 * 2. 卸载服务：node windows-service.js --uninstall
 * 
 * 注意：可能需要以管理员身份运行命令
 */ 