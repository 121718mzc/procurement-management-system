# 测试登录功能和token验证
from flask import Flask, request
from models.user import User
from models.role import Role, Permission
from db import db
from utils.auth import verify_token, require_permission
from routes.user import generate_token
from app import app

with app.app_context():
    # 测试1：检查admin用户是否存在
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print('✓ Admin user found:', admin.username)
        print('✓ Admin roles:', [role.name for role in admin.roles])
        
        # 测试2：检查admin用户是否有价格管理和合同管理权限
        has_pricing_view = admin.has_permission('pricing:view')
        has_contract_view = admin.has_permission('contract:view')
        print('✓ Admin has pricing:view permission:', has_pricing_view)
        print('✓ Admin has contract:view permission:', has_contract_view)
        
        # 测试3：生成token
        token = generate_token(admin.id)
        token_str = token.decode('utf-8') if isinstance(token, bytes) else token
        print('✓ Token generated:', token_str)
        
        # 测试4：验证token
        # 模拟请求头
        class MockRequest:
            def __init__(self, token):
                self.headers = {'Authorization': f'Bearer {token}'}
        
        # 替换request
        original_request = request
        try:
            # 模拟请求
            app.test_request_context()
            from flask import _request_ctx_stack
            ctx = _request_ctx_stack.top
            if ctx:
                ctx.request = MockRequest(token_str)
            
            # 验证token
            user = verify_token()
            print('✓ Token verification result:', user is not None)
            if user:
                print('✓ User found from token:', user.username)
        finally:
            # 恢复原始request
            if original_request:
                from flask import _request_ctx_stack
                ctx = _request_ctx_stack.top
                if ctx:
                    ctx.request = original_request
    else:
        print('✗ Admin user not found')

    # 测试5：检查所有权限是否存在
    permissions = Permission.query.all()
    print('\n✓ All permissions:')
    for perm in permissions:
        print(f'  - {perm.code}: {perm.name}')

    # 测试6：检查所有角色是否存在
    roles = Role.query.all()
    print('\n✓ All roles:')
    for role in roles:
        print(f'  - {role.name}: {len(role.permissions)} permissions')
