#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask服务主入口文件 (兼容模式)
此文件为兼容旧的入口点，实际应用使用app_factory.py创建应用
"""

import os
import sys
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 如果当前目录不在Python路径中，添加它
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入应用工厂
from app_factory import create_app

# 从环境变量获取配置名称
config_name = os.environ.get('FLASK_ENV', 'default')

# 创建应用实例
app = create_app(config_name)

# 如果作为主程序运行
if __name__ == '__main__':
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)
    
    # 输出启动信息
    print(f"启动Markdown同步服务器，监听 {host}:{port}")
    print(f"配置模式: {config_name}")
    print(f"调试模式: {'开启' if debug else '关闭'}")
    print(f"存储目录: {app.config.get('STORAGE_FOLDER')}")
    print(f"版本控制: {'开启' if app.config.get('ENABLE_VERSIONING') else '关闭'}")
    
    # 启动应用
    app.run(host=host, port=port, debug=debug) 