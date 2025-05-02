/**
 * 本地配置文件示例
 * 复制此文件为 config.local.js 以应用本地配置
 */

const path = require('path');

module.exports = {
  // 监控的文件夹路径 (绝对路径或相对路径)
  watchDir: path.resolve(__dirname, 'markdown_files'),
  
  // 服务器API接口 - 注意：这里应该只包含 API 的基础路径，不要包含 /sync 部分
  apiEndpoint: 'http://127.0.0.1:5000/api',
  
  // API认证令牌
  apiToken: 'd41d8cd98f00b204e9800998ecf8427e',
  
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
    'drafts/**',
    '.versions/**',
    '**/.DS_Store'
  ],
  
  // 文件类型过滤
  // 如果设置了此项，只会处理指定类型的文件
  // 如果为空或注释掉，则处理所有文件类型
  fileTypes: [
    '.md', '.txt',              // 文本文件
    '.png', '.jpg', '.jpeg',    // 图片文件
    '.pdf', '.docx'             // 文档文件
  ],
  
  // 排除的文件类型
  // 如果设置了此项，将不会处理指定类型的文件
  // 注意：如果同时设置了fileTypes，则此项不生效
  // excludeFileTypes: ['.exe', '.dll', '.zip', '.rar'],
  
  // 是否开启调试模式
  debug: true,
}; 