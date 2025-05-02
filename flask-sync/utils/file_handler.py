#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import logging
import datetime
import hashlib
import mimetypes
import base64
from flask import current_app

logger = logging.getLogger(__name__)

def save_file(file_path, content, is_binary=False):
    """
    保存任意类型文件
    
    Args:
        file_path (str): 文件的相对路径
        content (str): 文件内容（二进制文件可以是base64编码的字符串）
        is_binary (bool): 是否为二进制文件
        
    Returns:
        str: 保存的文件完整路径
    """
    # 获取文件完整路径
    full_path = os.path.join(current_app.config['STORAGE_FOLDER'], file_path)
    
    # 确保目录存在
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # 如果启用了版本控制，保存旧版本
    if current_app.config.get('ENABLE_VERSIONING', False) and os.path.exists(full_path):
        backup_file(full_path)
    
    # 写入文件内容
    if is_binary:
        try:
            # 如果是base64编码的内容，先解码
            binary_content = base64.b64decode(content)
            with open(full_path, 'wb') as f:
                f.write(binary_content)
        except Exception as e:
            logger.error(f"保存二进制文件失败: {str(e)}")
            raise
    else:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    logger.info(f"已保存文件: {file_path}")
    return full_path


def delete_file(file_path):
    """
    删除任意类型文件
    
    Args:
        file_path (str): 文件的相对路径
        
    Returns:
        bool: 删除成功返回True，文件不存在返回False
    """
    # 获取文件完整路径
    full_path = os.path.join(current_app.config['STORAGE_FOLDER'], file_path)
    
    # 检查文件是否存在
    if not os.path.exists(full_path):
        logger.warning(f"尝试删除不存在的文件: {file_path}")
        return False
    
    # 如果启用了版本控制，备份文件而不是直接删除
    if current_app.config.get('ENABLE_VERSIONING', False):
        backup_file(full_path, is_deletion=True)
    else:
        # 直接删除文件
        os.remove(full_path)
    
    logger.info(f"已删除文件: {file_path}")
    
    # 如果目录为空，删除目录（可选）
    try:
        dir_path = os.path.dirname(full_path)
        if os.path.exists(dir_path) and not os.listdir(dir_path):
            os.rmdir(dir_path)
            logger.info(f"已删除空目录: {os.path.dirname(file_path)}")
    except Exception as e:
        logger.error(f"删除空目录失败: {str(e)}")
    
    return True


def backup_file(file_path, is_deletion=False):
    """
    备份文件（版本控制）
    
    Args:
        file_path (str): 文件的完整路径
        is_deletion (bool): 是否为删除操作
        
    Returns:
        str: 备份文件的路径
    """
    # 确保文件存在
    if not os.path.exists(file_path):
        return None
    
    # 创建版本控制目录
    versions_dir = os.path.join(
        os.path.dirname(file_path), 
        '.versions',
        os.path.basename(file_path)
    )
    os.makedirs(versions_dir, exist_ok=True)
    
    # 计算文件哈希，用于版本命名
    file_hash = get_file_hash(file_path)
    
    # 创建版本文件名
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    version_filename = f"{timestamp}_{file_hash[:8]}"
    if is_deletion:
        version_filename += "_deleted"
    version_path = os.path.join(versions_dir, version_filename)
    
    # 复制文件
    shutil.copy2(file_path, version_path)
    
    logger.info(f"已创建文件备份: {version_path}")
    
    # 删除原始文件（如果是删除操作）
    if is_deletion:
        os.remove(file_path)
    
    # 清理旧版本
    cleanup_old_versions(versions_dir)
    
    return version_path


def get_file_hash(file_path):
    """
    计算文件的SHA-256哈希值
    
    Args:
        file_path (str): 文件路径
        
    Returns:
        str: 文件的哈希值
    """
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def cleanup_old_versions(versions_dir):
    """
    清理旧版本文件，仅保留最新的N个版本
    
    Args:
        versions_dir (str): 版本目录路径
    """
    max_versions = current_app.config.get('MAX_VERSIONS', 10)
    
    # 获取所有版本文件
    if not os.path.exists(versions_dir):
        return
    
    versions = [os.path.join(versions_dir, f) for f in os.listdir(versions_dir)]
    versions.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # 删除超出限制的旧版本
    if len(versions) > max_versions:
        for old_version in versions[max_versions:]:
            try:
                os.remove(old_version)
                logger.info(f"已删除旧版本文件: {old_version}")
            except Exception as e:
                logger.error(f"删除旧版本文件失败: {str(e)}")


def read_file(file_path):
    """
    读取文件内容
    
    Args:
        file_path (str): 文件的相对路径
        
    Returns:
        tuple: (content, is_binary, mime_type)
            - content: 文件内容（二进制文件会被base64编码）
            - is_binary: 是否为二进制文件
            - mime_type: 文件的MIME类型
    """
    # 获取文件完整路径
    full_path = os.path.join(current_app.config['STORAGE_FOLDER'], file_path)
    
    # 检查文件是否存在
    if not os.path.exists(full_path):
        logger.warning(f"尝试读取不存在的文件: {file_path}")
        return None, False, None
    
    # 判断文件类型
    mime_type, encoding = mimetypes.guess_type(full_path)
    is_text = mime_type and mime_type.startswith('text') or file_path.endswith(('.md', '.txt', '.json', '.csv', '.xml', '.html', '.css', '.js'))
    
    # 读取文件内容
    if is_text:
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, False, mime_type
        except UnicodeDecodeError:
            # 如果UTF-8解码失败，则当作二进制文件处理
            pass
    
    # 读取为二进制并进行base64编码
    with open(full_path, 'rb') as f:
        binary_content = f.read()
    
    # Base64编码
    content = base64.b64encode(binary_content).decode('ascii')
    
    return content, True, mime_type


def is_binary_file(file_path):
    """
    判断文件是否为二进制
    
    Args:
        file_path (str): 文件的完整路径
        
    Returns:
        bool: 是否为二进制文件
    """
    mime_type, encoding = mimetypes.guess_type(file_path)
    if mime_type and mime_type.startswith('text'):
        return False
    
    # 常见文本文件扩展名
    text_extensions = ['.md', '.txt', '.json', '.csv', '.xml', '.html', '.css', '.js', '.py', '.c', '.cpp', '.h', '.java']
    for ext in text_extensions:
        if file_path.endswith(ext):
            return False
    
    # 尝试读取文件开头字节判断
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk  # 包含空字节可能是二进制文件
    except:
        return True


# 保持向后兼容的函数别名
save_markdown_file = save_file
delete_markdown_file = delete_file
read_markdown_file = lambda path: read_file(path)[0] 