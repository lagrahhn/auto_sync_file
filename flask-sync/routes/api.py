#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import datetime
from flask import Blueprint, request, jsonify, current_app, Response, send_file
from utils.auth import token_required
from utils.file_handler import (
    save_file, 
    delete_file, 
    read_file,
    is_binary_file
)

# 创建蓝图
api_bp = Blueprint('api', __name__)
logger = logging.getLogger(__name__)


@api_bp.route('/sync', methods=['POST'])
@token_required
def sync_file():
    """
    处理文件同步请求
    支持的操作: add, change, delete
    支持所有文件类型，包括二进制文件
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "无效的请求数据"}), 400
        
        required_fields = ['action', 'path', 'timestamp']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"缺少必要字段: {field}"}), 400
        
        action = data['action']
        file_path = data['path']
        timestamp = data['timestamp']
        content = data.get('content')
        is_binary = data.get('is_binary', False)
        
        # 记录同步操作
        logger.info(f"收到同步请求: {action} - {file_path} - 二进制: {is_binary}")
        
        # 根据操作类型处理文件
        if action in ['add', 'change']:
            if content is None:
                return jsonify({"error": "添加或修改操作需要提供文件内容"}), 400
            
            # 保存文件
            full_path = save_file(file_path, content, is_binary)
            
            return jsonify({
                "status": "success",
                "message": f"文件 {action} 成功",
                "path": file_path,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
        elif action == 'delete':
            # 删除文件
            delete_file(file_path)
            
            return jsonify({
                "status": "success",
                "message": "文件删除成功",
                "path": file_path,
                "timestamp": datetime.datetime.now().isoformat()
            })
            
        else:
            return jsonify({"error": f"不支持的操作类型: {action}"}), 400
            
    except Exception as e:
        logger.exception(f"处理同步请求时出错: {str(e)}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


@api_bp.route('/status', methods=['GET'])
@token_required
def get_status():
    """获取服务状态"""
    storage_folder = current_app.config['STORAGE_FOLDER']
    
    # 获取存储统计信息
    total_files = 0
    total_size = 0
    file_types = {}
    
    for root, dirs, files in os.walk(storage_folder):
        # 跳过版本控制目录
        if '.versions' in root:
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            # 统计文件类型
            ext = os.path.splitext(file)[1].lower()
            if ext in file_types:
                file_types[ext] += 1
            else:
                file_types[ext] = 1
                
            total_files += 1
            total_size += os.path.getsize(file_path)
    
    return jsonify({
        "status": "running",
        "version": current_app.config['VERSION'],
        "storage_path": storage_folder,
        "files_count": total_files,
        "file_types": file_types,
        "storage_size_bytes": total_size,
        "storage_size_mb": round(total_size / (1024 * 1024), 2),
        "versioning_enabled": current_app.config.get('ENABLE_VERSIONING', False),
        "timestamp": datetime.datetime.now().isoformat()
    })


@api_bp.route('/files', methods=['GET'])
@token_required
def list_files():
    """列出所有同步的文件"""
    try:
        files_list = []
        storage_folder = current_app.config['STORAGE_FOLDER']
        
        for root, dirs, files in os.walk(storage_folder):
            # 跳过版本控制目录
            if '.versions' in root:
                continue
                
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, storage_folder)
                file_stat = os.stat(file_path)
                
                # 获取MIME类型
                import mimetypes
                mime_type, encoding = mimetypes.guess_type(file_path)
                is_binary = is_binary_file(file_path)
                
                files_list.append({
                    "path": rel_path,
                    "size": file_stat.st_size,
                    "size_formatted": format_size(file_stat.st_size),
                    "modified": datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat(),
                    "is_binary": is_binary,
                    "mime_type": mime_type
                })
        
        return jsonify({
            "status": "success",
            "count": len(files_list),
            "files": files_list
        })
        
    except Exception as e:
        logger.exception(f"列出文件时出错: {str(e)}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


@api_bp.route('/file/<path:file_path>', methods=['GET'])
@token_required
def get_file(file_path):
    """获取文件内容（支持所有文件类型）"""
    try:
        # 格式参数
        format_param = request.args.get('format', 'json')
        
        # 获取文件完整路径
        full_path = os.path.join(current_app.config['STORAGE_FOLDER'], file_path)
        
        # 检查文件是否存在
        if not os.path.exists(full_path):
            return jsonify({"error": "文件不存在"}), 404
            
        # 如果请求直接下载
        if format_param == 'raw':
            return send_file(full_path, as_attachment=True)
            
        # 读取文件内容
        content, is_binary, mime_type = read_file(file_path)
        
        if content is None:
            return jsonify({"error": "文件不存在或无法读取"}), 404
        
        return jsonify({
            "status": "success",
            "path": file_path,
            "content": content,
            "is_binary": is_binary,
            "mime_type": mime_type,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.exception(f"获取文件内容时出错: {str(e)}")
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB" 