#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Markdown同步服务器')
    
    parser.add_argument('--host', type=str, default=os.environ.get('FLASK_HOST', '0.0.0.0'),
                        help='监听主机 (默认: 0.0.0.0)')
    
    parser.add_argument('--port', type=int, default=int(os.environ.get('FLASK_PORT', 5000)),
                        help='监听端口 (默认: 5000)')
    
    parser.add_argument('--debug', action='store_true', default=os.environ.get('FLASK_DEBUG', '').lower() in ('true', '1', 't'),
                        help='启用调试模式')
    
    parser.add_argument('--env', type=str, choices=['development', 'production', 'testing'],
                        default=os.environ.get('FLASK_ENV', 'development'),
                        help='环境类型 (默认: development)')
    
    parser.add_argument('--storage', type=str, default=os.environ.get('STORAGE_FOLDER', ''),
                        help='Markdown文件存储目录')
    
    parser.add_argument('--token', type=str, default=os.environ.get('API_TOKENS', ''),
                        help='API令牌，多个令牌用逗号分隔')
    
    parser.add_argument('--versioning', action='store_true', 
                        default=os.environ.get('ENABLE_VERSIONING', '').lower() in ('true', '1', 't'),
                        help='启用文件版本控制')
    
    return parser.parse_args()


def main():
    """主入口函数"""
    args = parse_args()
    
    # 设置环境变量
    os.environ['FLASK_ENV'] = args.env
    os.environ['FLASK_DEBUG'] = str(args.debug).lower()
    os.environ['FLASK_HOST'] = args.host
    os.environ['FLASK_PORT'] = str(args.port)
    
    if args.storage:
        os.environ['STORAGE_FOLDER'] = args.storage
    
    if args.token:
        os.environ['API_TOKENS'] = args.token
    
    os.environ['ENABLE_VERSIONING'] = str(args.versioning).lower()
    
    # 导入应用(这里延迟导入是为了先应用环境变量)
    from wsgi import app
    
    # 启动应用
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)
    except Exception as e:
        logging.exception("启动服务器时出错")
        sys.exit(1) 