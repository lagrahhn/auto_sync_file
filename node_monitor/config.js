const path = require('path');
const fs = require('fs-extra');

// 默认配置
const defaultConfig = {
  // 监控的文件夹路径
  watchDir: path.resolve(__dirname, 'markdown'),
  
  // 服务器API接口
  apiEndpoint: 'http://example.com/api/sync',
  
  // API认证令牌
  apiToken: 'your_api_token',
  
  // 重试次数
  retryCount: 3,
  
  // 重试间隔（毫秒）
  retryInterval: 5000,
  
  // 忽略的文件或文件夹（使用逗号分隔）
  ignorePatterns: [
    'node_modules', 
    'temp', 
    '*.tmp', 
    '.git',
    '.versions/**',
    '**/.DS_Store'
  ],
  
  // 默认处理所有文件类型
  // 如果需要限制特定类型，在config.local.js中配置
  fileTypes: [],
  
  // 默认不排除任何文件类型
  excludeFileTypes: [],
  
  // 是否开启调试模式
  debug: false,
};

// 尝试加载用户自定义配置
let userConfig = {};
const userConfigPath = path.join(__dirname, 'config.local.js');

try {
  if (fs.existsSync(userConfigPath)) {
    userConfig = require('./config.local.js');
    if (defaultConfig.debug || userConfig.debug) {
      console.log('已加载自定义配置文件');
    }
  }
} catch (err) {
  console.error('加载自定义配置文件失败:', err);
}

// 合并配置
const config = { ...defaultConfig, ...userConfig };

// 处理环境变量覆盖
if (process.env.WATCH_DIR) {
  config.watchDir = path.resolve(process.env.WATCH_DIR);
}
if (process.env.API_ENDPOINT) {
  config.apiEndpoint = process.env.API_ENDPOINT;
}
if (process.env.API_TOKEN) {
  config.apiToken = process.env.API_TOKEN;
}
if (process.env.RETRY_COUNT) {
  config.retryCount = parseInt(process.env.RETRY_COUNT, 10);
}
if (process.env.RETRY_INTERVAL) {
  config.retryInterval = parseInt(process.env.RETRY_INTERVAL, 10);
}
if (process.env.IGNORE_PATTERNS) {
  config.ignorePatterns = process.env.IGNORE_PATTERNS.split(',').map(p => p.trim());
}
if (process.env.DEBUG) {
  config.debug = process.env.DEBUG.toLowerCase() === 'true';
}
if (process.env.FILE_TYPES) {
  config.fileTypes = process.env.FILE_TYPES.split(',').map(p => p.trim());
}

module.exports = config; 