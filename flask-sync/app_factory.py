#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config import config

def create_app(config_name='default'):
    """
    创建Flask应用实例
    
    Args:
        config_name (str): 配置名称，可选值：development, production, testing, default
        
    Returns:
        Flask: Flask应用实例
    """
    app = Flask(__name__)
    
    # 加载配置
    app_config = config.get(config_name, config['default'])
    app.config.from_object(app_config)
    
    # 初始化应用配置
    app_config.init_app(app)
    
    # 配置日志
    setup_logging(app)
    
    # 配置CORS
    if app.config.get('ENABLE_CORS', True):
        cors_origins = app.config.get('CORS_ORIGINS', '*')
        CORS(app, resources={r"/api/*": {"origins": cors_origins}})
    
    # 注册蓝图
    from routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 注册错误处理
    register_error_handlers(app)
    
    return app


def setup_logging(app):
    """配置应用日志"""
    log_level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    log_folder = app.config.get('LOG_FOLDER', 'logs')
    
    # 确保日志目录存在
    os.makedirs(log_folder, exist_ok=True)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_folder, 'app.log')),
            logging.StreamHandler()
        ]
    )
    
    # 设置第三方库日志级别
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)


def register_error_handlers(app):
    """注册全局错误处理器"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "请求错误",
            "message": str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "error": "未授权访问",
            "message": str(error)
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "error": "禁止访问",
            "message": str(error)
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "资源未找到",
            "message": str(error)
        }), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": "服务器内部错误",
            "message": str(error)
        }), 500 