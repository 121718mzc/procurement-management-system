# 权限验证装饰器
from functools import wraps
from flask import request, jsonify
import jwt
import os
from models.user import User

# 固定的密钥，实际生产环境中应该从环境变量获取
SECRET_KEY = b'your-secret-key-here-123456789'

# 验证token
def verify_token():
    """验证token并返回用户对象"""
    token = request.headers.get('Authorization')
    if not token:
        print('No token provided')
        return None
    
    try:
        print(f'Token received: {token}')
        # 移除Bearer前缀（如果存在）
        if token.startswith('Bearer '):
            token = token[7:]
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(f'Decoded payload: {payload}')
        user_id = payload.get('user_id')
        user = User.query.get(user_id)
        print(f'User found: {user}')
        return user
    except Exception as e:
        print(f'Token verification error: {str(e)}')
        return None

# 权限验证装饰器
def require_permission(permission_code):
    """需要特定权限的装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 验证token
            user = verify_token()
            if not user:
                return jsonify({'message': '未授权访问'}), 401
            
            # 检查用户是否有指定权限
            if not user.has_permission(permission_code):
                return jsonify({'message': '权限不足'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 角色验证装饰器
def require_role(role_name):
    """需要特定角色的装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 验证token
            user = verify_token()
            if not user:
                return jsonify({'message': '未授权访问'}), 401
            
            # 检查用户是否有指定角色
            has_role = any(role.name == role_name for role in user.roles)
            if not has_role:
                return jsonify({'message': '角色不足'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator