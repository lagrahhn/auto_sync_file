/**
 * 本地配置文件示例
 * 复制此文件为 config.local.js 以应用本地配置
 */

const path = require('path');

module.exports = {
  // 监控的文件夹路径 (绝对路径或相对路径)
  watchDir: path.resolve(__dirname, 'markdown_files'),
  
  // 服务器API接口
  apiEndpoint: 'http://your-server.com/api',
  
  // API认证令牌
  apiToken: 'your_secret_token',
  
  // 重试次数
  retryCount: 5,
  
  // 重试间隔（毫秒）
  retryInterval: 3000,
  
  // 忽略的文件或文件夹
  ignorePatterns: [
    'node_modules',
    '.git',
    '*.tmp',
    'temp/**',
    'drafts/**'
  ],
  
  // 是否开启调试模式
  debug: true,
}; 