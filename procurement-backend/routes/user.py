# 用户路由
from flask import Blueprint, request, jsonify
from models.user import User
from db import db
import jwt
import os
from datetime import datetime, timedelta

# 创建蓝图
bp = Blueprint('user', __name__, url_prefix='/user')

# 生成token
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, os.urandom(24), algorithm='HS256')

# 用户登录
@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        user = User.query.filter_by(username=data.get('username')).first()
        if not user or not user.check_password(data.get('password')):
            return jsonify({'message': '用户名或密码错误'}), 401
        
        token = generate_token(user.id)
        return jsonify({'message': '登录成功', 'token': token, 'user': user.to_dict()})
    except Exception as e:
        return jsonify({'message': '登录失败', 'error': str(e)}), 400

# 用户信息
@bp.route('/info', methods=['GET'])
def get_user_info():
    try:
        # 这里简化处理，实际应该从token中获取用户ID
        user = User.query.filter_by(username='buyer').first()
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({'message': '获取用户信息失败', 'error': str(e)}), 400

# 初始化默认用户
@bp.route('/init', methods=['POST'])
def init_user():
    try:
        # 检查是否已存在用户
        existing_user = User.query.filter_by(username='buyer').first()
        if existing_user:
            return jsonify({'message': '默认用户已存在'})
        
        # 创建默认用户
        user = User(
            username='buyer',
            name='采购员',
            status='active'
        )
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': '默认用户创建成功', 'user': user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '默认用户创建失败', 'error': str(e)}), 400
