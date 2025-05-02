@echo off
echo 启动Markdown同步服务器...

REM 检查虚拟环境是否存在
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 创建必要的目录
if not exist markdown_files mkdir markdown_files
if not exist logs mkdir logs

REM 启动应用
echo 启动Markdown同步服务器...
python run.py %*

pause 