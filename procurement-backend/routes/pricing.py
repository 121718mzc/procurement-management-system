# 价格管理路由
from flask import Blueprint, request, jsonify
from models.pricing import Pricing
from db import db
from utils.auth import require_permission

# 创建蓝图
bp = Blueprint('pricing', __name__, url_prefix='/pricing')

# 价格列表
@bp.route('/', methods=['GET'])
@require_permission('pricing:view')
def get_pricings():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 分页查询
        pricings = Pricing.query.paginate(page=page, per_page=per_page, error_out=False)
        
        # 构建响应
        result = []
        for pricing in pricings.items:
            result.append(pricing.to_dict())
        
        return jsonify({
            'data': result,
            'total': pricings.total,
            'page': pricings.page,
            'per_page': pricings.per_page,
            'pages': pricings.pages
        })
    except Exception as e:
        print(f"Error in get_pricings: {e}")
        return jsonify({'message': '获取价格列表失败', 'error': str(e)}), 500

# 添加价格
@bp.route('/', methods=['POST'])
@require_permission('pricing:add')
def add_pricing():
    data = request.json
    try:
        pricing = Pricing(
            supplier_id=data['supplier_id'],
            material_id=data['material_id'],
            price=data['price'],
            effective_date=data['effective_date'],
            expiry_date=data['expiry_date'],
            status=data.get('status', 'active')
        )
        db.session.add(pricing)
        db.session.commit()
        return jsonify({'message': '价格添加成功', 'data': pricing.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '价格添加失败', 'error': str(e)}), 400

# 编辑价格
@bp.route('/<int:id>', methods=['PUT'])
@require_permission('pricing:edit')
def update_pricing(id):
    data = request.json
    try:
        pricing = Pricing.query.get(id)
        if not pricing:
            return jsonify({'message': '价格不存在'}), 404
        
        pricing.supplier_id = data.get('supplier_id', pricing.supplier_id)
        pricing.material_id = data.get('material_id', pricing.material_id)
        pricing.price = data.get('price', pricing.price)
        pricing.effective_date = data.get('effective_date', pricing.effective_date)
        pricing.expiry_date = data.get('expiry_date', pricing.expiry_date)
        pricing.status = data.get('status', pricing.status)
        
        db.session.commit()
        return jsonify({'message': '价格更新成功', 'data': pricing.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '价格更新失败', 'error': str(e)}), 400

# 删除价格
@bp.route('/<int:id>', methods=['DELETE'])
@require_permission('pricing:delete')
def delete_pricing(id):
    try:
        pricing = Pricing.query.get(id)
        if not pricing:
            return jsonify({'message': '价格不存在'}), 404
        
        db.session.delete(pricing)
        db.session.commit()
        return jsonify({'message': '价格删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '价格删除失败', 'error': str(e)}), 400
