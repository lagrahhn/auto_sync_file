# Markdown自动同步工具

这是一个用于监控Markdown文件并与服务端同步的工具。它可以自动检测文件的添加、修改和删除，并将这些变更同步到服务器。

## 功能特点

- 监控指定目录下的Markdown文件变更
- 自动同步新增、修改和删除的文件
- 支持服务端API同步
- 失败重试机制
- PM2守护进程支持
- 开机自启动支持
- Windows服务支持
- 可自定义配置

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/markdown-sync.git
cd markdown-sync
```

2. 使用自动安装脚本（推荐）：

```bash
npm run setup
```

此脚本将引导您完成安装依赖、创建配置文件和设置PM2的过程。

3. 手动安装：

```bash
# 安装依赖
npm install

# 全局安装PM2（如果尚未安装）
npm install pm2 -g
```

## 配置

你可以通过以下方式自定义配置：

1. 编辑`config.js`文件中的默认配置
2. 创建`config.local.js`文件进行本地覆盖配置（可以复制`config.local.example.js`文件并修改）
3. 使用环境变量

主要配置项：

- `watchDir`: 要监控的文件夹路径
- `apiEndpoint`: 服务器API接口
- `apiToken`: API认证令牌
- `retryCount`: 同步失败重试次数
- `retryInterval`: 重试间隔（毫秒）
- `ignorePatterns`: 忽略的文件或文件夹
- `debug`: 是否开启调试模式

## 使用方法

### 快速命令

本项目提供了多种便捷的npm脚本命令：

```bash
# 常规启动
npm start

# 开发模式（自动重启）
npm run dev

# 运行安装向导
npm run setup

# 配置开机自启动
npm run startup

# PM2相关命令
npm run pm2:start    # 使用PM2启动
npm run pm2:stop     # 停止服务
npm run pm2:restart  # 重启服务
npm run pm2:status   # 查看状态
npm run pm2:logs     # 查看日志
npm run pm2:monitor  # 打开监控面板

# Windows服务相关命令
npm run win-service:install    # 安装为Windows服务
npm run win-service:uninstall  # 卸载Windows服务
```

### 手动启动与管理

如果你熟悉PM2，也可以直接使用PM2命令：

```bash
# 使用PM2启动（推荐用于生产环境）
pm2 start ecosystem.config.js

# 配置开机自启动
pm2 startup
pm2 save
```

## 日志

PM2将自动管理日志文件，可以通过以下方式查看：

```bash
# 通过npm脚本
npm run pm2:logs

# 或直接使用PM2命令
pm2 logs markdown-sync
```

## 开机自启动

为了确保服务在系统重启后自动运行，你可以：

```bash
# 使用助手脚本（推荐）
npm run startup

# 或手动配置
pm2 startup
pm2 save
```

在Windows系统上，可能需要以管理员身份运行生成的命令或创建计划任务。

## Windows系统专用设置

在Windows系统上，除了使用PM2之外，还可以将应用安装为Windows服务：

```bash
# 安装为Windows服务（需要管理员权限）
npm run win-service:install

# 卸载Windows服务
npm run win-service:uninstall
```

安装为Windows服务后，应用将在系统启动时自动运行，且可以在Windows服务管理器中查看和控制。

## 许可证

ISC 