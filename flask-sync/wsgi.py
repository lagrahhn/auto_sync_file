#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app_factory import create_app

# 从环境变量获取配置
config_name = os.environ.get('FLASK_ENV', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', False)
    
    print(f"启动Markdown同步服务器，监听 {host}:{port}")
    print(f"配置模式: {config_name}")
    print(f"调试模式: {'开启' if debug else '关闭'}")
    print(f"存储目录: {app.config.get('STORAGE_FOLDER')}")
    print(f"版本控制: {'开启' if app.config.get('ENABLE_VERSIONING') else '关闭'}")
    
    app.run(host=host, port=port, debug=debug) 