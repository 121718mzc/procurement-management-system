# 角色和权限路由
from flask import Blueprint, request, jsonify
from models.role import Role, Permission
from models.user import User
from db import db

# 创建蓝图
bp = Blueprint('role', __name__, url_prefix='/role')

# 获取所有角色
@bp.route('/', methods=['GET'])
def get_roles():
    try:
        roles = Role.query.all()
        return jsonify({
            'data': [role.to_dict() for role in roles],
            'total': len(roles)
        })
    except Exception as e:
        return jsonify({'message': '获取角色列表失败', 'error': str(e)}), 500

# 获取所有权限
@bp.route('/permission', methods=['GET'])
def get_permissions():
    try:
        permissions = Permission.query.all()
        return jsonify({
            'data': [permission.to_dict() for permission in permissions],
            'total': len(permissions)
        })
    except Exception as e:
        return jsonify({'message': '获取权限列表失败', 'error': str(e)}), 500

# 创建角色
@bp.route('/', methods=['POST'])
def create_role():
    data = request.json
    try:
        role = Role(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(role)
        db.session.commit()
        return jsonify({'message': '角色创建成功', 'data': role.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '角色创建失败', 'error': str(e)}), 400

# 创建权限
@bp.route('/permission', methods=['POST'])
def create_permission():
    data = request.json
    try:
        permission = Permission(
            name=data['name'],
            code=data['code'],
            description=data.get('description')
        )
        db.session.add(permission)
        db.session.commit()
        return jsonify({'message': '权限创建成功', 'data': permission.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '权限创建失败', 'error': str(e)}), 400

# 为角色分配权限
@bp.route('/<int:role_id>/permission', methods=['POST'])
def assign_permission(role_id):
    data = request.json
    try:
        role = Role.query.get(role_id)
        if not role:
            return jsonify({'message': '角色不存在'}), 404
        
        # 清空现有权限
        role.permissions = []
        
        # 添加新权限
        for permission_id in data.get('permission_ids', []):
            permission = Permission.query.get(permission_id)
            if permission:
                role.permissions.append(permission)
        
        db.session.commit()
        return jsonify({'message': '权限分配成功', 'data': role.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '权限分配失败', 'error': str(e)}), 400

# 为用户分配角色
@bp.route('/user/<int:user_id>', methods=['POST'])
def assign_role(user_id):
    data = request.json
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        
        # 清空现有角色
        user.roles = []
        
        # 添加新角色
        for role_id in data.get('role_ids', []):
            role = Role.query.get(role_id)
            if role:
                user.roles.append(role)
        
        db.session.commit()
        return jsonify({'message': '角色分配成功', 'data': user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '角色分配失败', 'error': str(e)}), 400

# 初始化默认角色和权限
@bp.route('/init', methods=['POST'])
def init_roles():
    try:
        # 检查是否已存在角色
        existing_role = Role.query.first()
        if existing_role:
            return jsonify({'message': '默认角色已存在'})
        
        # 创建默认权限
        permissions = [
            {'name': '查看供应商', 'code': 'supplier:view'},
            {'name': '添加供应商', 'code': 'supplier:add'},
            {'name': '编辑供应商', 'code': 'supplier:edit'},
            {'name': '删除供应商', 'code': 'supplier:delete'},
            {'name': '查看物料', 'code': 'material:view'},
            {'name': '添加物料', 'code': 'material:add'},
            {'name': '编辑物料', 'code': 'material:edit'},
            {'name': '删除物料', 'code': 'material:delete'},
            {'name': '查看价格', 'code': 'pricing:view'},
            {'name': '添加价格', 'code': 'pricing:add'},
            {'name': '编辑价格', 'code': 'pricing:edit'},
            {'name': '删除价格', 'code': 'pricing:delete'},
            {'name': '查看合同', 'code': 'contract:view'},
            {'name': '添加合同', 'code': 'contract:add'},
            {'name': '编辑合同', 'code': 'contract:edit'},
            {'name': '删除合同', 'code': 'contract:delete'},
            {'name': '查看采购订单', 'code': 'purchase:view'},
            {'name': '添加采购订单', 'code': 'purchase:add'},
            {'name': '编辑采购订单', 'code': 'purchase:edit'},
            {'name': '删除采购订单', 'code': 'purchase:delete'},
            {'name': '管理用户', 'code': 'user:manage'},
            {'name': '管理角色', 'code': 'role:manage'}
        ]
        
        permission_objects = []
        for perm_data in permissions:
            permission = Permission(**perm_data)
            db.session.add(permission)
            permission_objects.append(permission)
        
        # 创建默认角色
        admin_role = Role(name='管理员', description='系统管理员，拥有所有权限')
        buyer_role = Role(name='采购员', description='采购人员，拥有采购相关权限')
        
        # 为管理员分配所有权限
        admin_role.permissions = permission_objects
        
        # 为采购员分配采购相关权限
        buyer_permissions = [p for p in permission_objects if p.code.startswith('supplier:') or p.code.startswith('material:') or p.code.startswith('pricing:') or p.code.startswith('contract:') or p.code.startswith('purchase:')]
        buyer_role.permissions = buyer_permissions
        
        db.session.add(admin_role)
        db.session.add(buyer_role)
        db.session.commit()
        
        # 为默认用户分配角色
        default_user = User.query.filter_by(username='buyer').first()
        if default_user:
            default_user.roles.append(buyer_role)
            db.session.commit()
        
        return jsonify({'message': '默认角色和权限初始化成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '默认角色和权限初始化失败', 'error': str(e)}), 400