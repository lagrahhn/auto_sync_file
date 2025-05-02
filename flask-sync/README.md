# Markdown同步服务端

这是一个基于Flask的服务端应用，用于接收和处理客户端同步的Markdown文件。该服务与Node.js客户端配合使用，支持文件的添加、修改和删除操作。

## 功能特点

- 基于Flask的轻量级API服务
- 支持Markdown文件的添加、修改、删除同步
- 提供API令牌认证机制
- 可选文件版本控制功能
- 灵活的配置选项
- 支持Docker容器化部署
- CORS跨域支持

## 安装与运行

### 前提条件

- Python 3.7+
- pip

### 安装步骤

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/flask-sync.git
cd flask-sync
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置环境变量：

复制环境变量示例文件并修改：

```bash
# Windows
copy .env.sample .env

# Linux/macOS
cp .env.sample .env
```

编辑.env文件，设置API令牌与Node.js客户端匹配：

```
API_TOKENS=your_api_token
```

### 运行服务器

```bash
# 开发模式
python run.py --debug

# 生产模式
python run.py --env production

# 查看所有选项
python run.py --help
```

## 使用Docker运行

### 使用Dockerfile

```bash
# 构建镜像
docker build -t markdown-sync .

# 运行容器
docker run -p 5000:5000 -v $(pwd)/markdown_files:/app/markdown_files markdown-sync
```

### 使用Docker Compose

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## API接口

### 1. 同步文件

```
POST /api/sync
```

请求头：
```
Authorization: Bearer your_api_token
```

请求体：
```json
{
  "action": "add|change|delete",
  "path": "relative/path/to/file.md",
  "content": "Markdown content here",
  "timestamp": "2023-05-01T12:34:56.789Z"
}
```

### 2. 获取状态

```
GET /api/status
```

### 3. 列出所有文件

```
GET /api/files
```

### 4. 获取文件内容

```
GET /api/file/{file_path}
```

## 配置选项

服务器支持多种配置方式，优先级从高到低：

1. 命令行参数
2. 环境变量
3. .env文件
4. 默认值

主要配置项：

- API_TOKENS: API访问令牌（必须与Node.js客户端配置相同）
- STORAGE_FOLDER: Markdown文件存储目录
- ENABLE_VERSIONING: 是否启用文件版本控制
- MAX_VERSIONS: 保留的最大版本数量

## 与Node.js客户端集成

要将此服务与Node.js客户端集成，确保：

1. 客户端的API令牌与服务端匹配
2. 客户端的API端点指向此服务的URL

在Node.js客户端配置：

```js
module.exports = {
  apiEndpoint: 'http://your-server-ip:5000/api/sync',
  apiToken: 'your_api_token',
  // 其他配置...
};
```

## 许可证

ISC 