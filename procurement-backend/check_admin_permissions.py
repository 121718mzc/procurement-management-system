# 检查admin用户的权限
from db import db
from models.user import User
from models.role import Role, Permission
from app import app

with app.app_context():
    # 获取admin用户
    admin = User.query.filter_by(username='admin').first()
    if admin:
        print('Admin user:', admin)
        print('Admin roles:', [role.name for role in admin.roles])
        
        # 获取管理员角色
        admin_role = Role.query.filter_by(name='管理员').first()
        if admin_role:
            print('Admin role permissions:', [perm.code for perm in admin_role.permissions])
            
            # 检查是否有价格管理和合同管理的权限
            pricing_permissions = [perm.code for perm in admin_role.permissions if perm.code.startswith('pricing:')]
            contract_permissions = [perm.code for perm in admin_role.permissions if perm.code.startswith('contract:')]
            
            print('Pricing permissions:', pricing_permissions)
            print('Contract permissions:', contract_permissions)
        else:
            print('Admin role not found')
    else:
        print('Admin user not found')
