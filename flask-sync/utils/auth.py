#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import logging
from flask import request, jsonify, current_app

logger = logging.getLogger(__name__)

def token_required(f):
    """
    装饰器：验证API访问令牌
    使用方式: @token_required
    """
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头中获取令牌
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            # 解析Bearer令牌
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        
        if not token:
            logger.warning("未提供API令牌")
            return jsonify({"error": "需要认证令牌"}), 401
            
        # 验证令牌
        if token not in current_app.config['API_TOKENS']:
            logger.warning(f"无效的API令牌: {token[:10]}...")
            return jsonify({"error": "无效的认证令牌"}), 401
            
        # 令牌有效，继续处理请求
        return f(*args, **kwargs)
        
    return decorated


def create_token(token_value):
    """
    生成新的API令牌
    这只是示例函数，实际应用中你可能需要更安全的令牌生成机制
    """
    import secrets
    
    if not token_value:
        # 生成随机令牌
        token = secrets.token_hex(32)
    else:
        token = token_value
        
    return token 