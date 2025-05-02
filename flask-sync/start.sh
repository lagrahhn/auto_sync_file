#!/bin/bash

# 创建虚拟环境(如果不存在)
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 创建必要的目录
mkdir -p markdown_files logs

# 启动应用
echo "启动Markdown同步服务器..."
python run.py "$@" 