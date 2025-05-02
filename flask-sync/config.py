#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import secrets

class Config:
    """Flask应用配置类"""
    
    # 应用信息
    VERSION = '1.0.0'
    
    # 服务器配置
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    
    # 存储配置
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STORAGE_FOLDER = os.environ.get('STORAGE_FOLDER', os.path.join(BASE_DIR, 'markdown_files'))
    LOG_FOLDER = os.environ.get('LOG_FOLDER', os.path.join(BASE_DIR, 'logs'))
    
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    
    # API令牌配置 - 你的NodeJS客户端中的API_TOKEN值必须与此匹配
    API_TOKENS = os.environ.get('API_TOKENS', 'd41d8cd98f00b204e9800998ecf8427e').split(',')
    
    # 版本控制配置
    ENABLE_VERSIONING = os.environ.get('ENABLE_VERSIONING', 'False').lower() in ('true', '1', 't')
    MAX_VERSIONS = int(os.environ.get('MAX_VERSIONS', 10))
    
    # CORS配置
    ENABLE_CORS = os.environ.get('ENABLE_CORS', 'True').lower() in ('true', '1', 't')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    @classmethod
    def init_app(cls, app):
        """初始化Flask应用的配置"""
        # 确保目录存在
        os.makedirs(cls.STORAGE_FOLDER, exist_ok=True)
        os.makedirs(cls.LOG_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    STORAGE_FOLDER = os.path.join(Config.BASE_DIR, 'test_files')


# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# 默认配置
app_config = config.get(os.environ.get('FLASK_ENV', 'default').lower(), DevelopmentConfig) 