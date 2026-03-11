# 检查并初始化admin用户
from db import db
from models.user import User
from models.role import Role
from app import app

with app.app_context():
    # 检查是否存在admin用户
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        # 创建admin用户
        admin = User(
            username='admin',
            name='管理员',
            status='active'
        )
        admin.set_password('123456')
        db.session.add(admin)
        db.session.commit()
        print('Admin user created successfully')
    else:
        print('Admin user already exists')
    
    # 检查是否存在管理员角色
    admin_role = Role.query.filter_by(name='管理员').first()
    if admin_role:
        # 为admin用户分配管理员角色
        if admin_role not in admin.roles:
            admin.roles.append(admin_role)
            db.session.commit()
            print('Admin role assigned to admin user')
        else:
            print('Admin user already has admin role')
    else:
        print('Admin role not found')
    
    # 打印admin用户信息
    print('Admin user:', admin)
    print('Admin roles:', [role.name for role in admin.roles])
