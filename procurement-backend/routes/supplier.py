# 供应商路由
from flask import Blueprint, request, jsonify
from models.supplier import Supplier
from db import db
from utils.auth import require_permission

# 创建蓝图
bp = Blueprint('supplier', __name__, url_prefix='/supplier')

# 供应商列表
@bp.route('/', methods=['GET'])
@require_permission('supplier:view')
def get_suppliers():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 分页查询
    suppliers = Supplier.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 构建响应
    result = []
    for supplier in suppliers.items:
        result.append(supplier.to_dict())
    
    return jsonify({
        'data': result,
        'total': suppliers.total,
        'page': suppliers.page,
        'per_page': suppliers.per_page,
        'pages': suppliers.pages
    })

# 添加供应商
@bp.route('/', methods=['POST'])
@require_permission('supplier:add')
def add_supplier():
    data = request.json
    try:
        supplier = Supplier(
            name=data['name'],
            contact_person=data['contact_person'],
            phone=data['phone'],
            email=data['email'],
            address=data['address'],
            status=data.get('status', 'active')
        )
        db.session.add(supplier)
        db.session.commit()
        return jsonify({'message': '供应商添加成功', 'data': supplier.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '供应商添加失败', 'error': str(e)}), 400

# 编辑供应商
@bp.route('/<int:id>', methods=['PUT'])
@require_permission('supplier:edit')
def update_supplier(id):
    data = request.json
    try:
        supplier = Supplier.query.get(id)
        if not supplier:
            return jsonify({'message': '供应商不存在'}), 404
        
        supplier.name = data.get('name', supplier.name)
        supplier.contact_person = data.get('contact_person', supplier.contact_person)
        supplier.phone = data.get('phone', supplier.phone)
        supplier.email = data.get('email', supplier.email)
        supplier.address = data.get('address', supplier.address)
        supplier.status = data.get('status', supplier.status)
        
        db.session.commit()
        return jsonify({'message': '供应商更新成功', 'data': supplier.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '供应商更新失败', 'error': str(e)}), 400

# 删除供应商
@bp.route('/<int:id>', methods=['DELETE'])
@require_permission('supplier:delete')
def delete_supplier(id):
    try:
        supplier = Supplier.query.get(id)
        if not supplier:
            return jsonify({'message': '供应商不存在'}), 404
        
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'message': '供应商删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '供应商删除失败', 'error': str(e)}), 400
