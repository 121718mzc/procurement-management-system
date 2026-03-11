# 采购订单路由
from flask import Blueprint, request, jsonify
from models.purchase_order import PurchaseOrder
from models.purchase_order_item import PurchaseOrderItem
from db import db
from utils.auth import require_permission

# 创建蓝图
bp = Blueprint('purchase', __name__, url_prefix='/purchase')

# 采购订单列表
@bp.route('/', methods=['GET'])
@require_permission('purchase:view')
def get_purchase_orders():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取搜索参数
        order_number = request.args.get('order_number', '')
        supplier_id = request.args.get('supplier_id', '')
        status = request.args.get('status', '')
        
        # 构建查询
        query = PurchaseOrder.query
        
        # 添加搜索条件
        if order_number:
            query = query.filter(PurchaseOrder.order_number.like(f'%{order_number}%'))
        if status:
            query = query.filter(PurchaseOrder.status == status)
        
        # 如果有供应商ID，通过合同关联查询
        if supplier_id:
            from models.contract import Contract
            query = query.join(Contract).filter(Contract.supplier_id == supplier_id)
        
        # 分页查询
        orders = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # 构建响应
        result = []
        for order in orders.items:
            result.append(order.to_dict())
        
        print(f"采购订单查询结果: {len(result)} 条记录")
        print(f"总记录数: {orders.total}")
        
        return jsonify({
            'data': result,
            'total': orders.total,
            'page': orders.page,
            'per_page': orders.per_page,
            'pages': orders.pages
        })
    except Exception as e:
        print(f"Error in get_purchase_orders: {e}")
        return jsonify({'message': '获取采购订单列表失败', 'error': str(e)}), 500

# 添加采购订单
@bp.route('/', methods=['POST'])
@require_permission('purchase:add')
def add_purchase_order():
    data = request.json
    try:
        # 创建采购订单
        order = PurchaseOrder(
            contract_id=data['contract_id'],
            supplier_id=data['supplier_id'],
            order_number=data['order_number'],
            order_date=data.get('order_date', db.func.current_date()),
            delivery_date=data.get('delivery_date', db.func.current_date()),
            status=data.get('status', 'pending')
        )
        db.session.add(order)
        db.session.flush()  # 获取order.id
        
        # 添加采购订单物品
        if 'items' in data:
            for item in data['items']:
                order_item = PurchaseOrderItem(
                    purchase_order_id=order.id,
                    material_id=item['material_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    total_price=item['total_price'],
                    status=data.get('status', 'pending')
                )
                db.session.add(order_item)
        
        db.session.commit()
        return jsonify({'message': '采购订单添加成功', 'data': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '采购订单添加失败', 'error': str(e)}), 400

# 编辑采购订单
@bp.route('/<int:id>', methods=['PUT'])
@require_permission('purchase:edit')
def update_purchase_order(id):
    data = request.json
    try:
        order = PurchaseOrder.query.get(id)
        if not order:
            return jsonify({'message': '采购订单不存在'}), 404
        
        # 更新采购订单信息
        order.contract_id = data.get('contract_id', order.contract_id)
        order.supplier_id = data.get('supplier_id', order.supplier_id)
        order.order_number = data.get('order_number', order.order_number)
        order.order_date = data.get('order_date', order.order_date)
        order.delivery_date = data.get('delivery_date', order.delivery_date)
        order.status = data.get('status', order.status)
        
        # 更新采购订单物品
        if 'items' in data:
            # 删除旧物品
            PurchaseOrderItem.query.filter_by(purchase_order_id=id).delete()
            # 添加新物品
            for item in data['items']:
                order_item = PurchaseOrderItem(
                    purchase_order_id=order.id,
                    material_id=item['material_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    total_price=item['total_price'],
                    status=data.get('status', 'pending')
                )
                db.session.add(order_item)
        
        db.session.commit()
        return jsonify({'message': '采购订单更新成功', 'data': order.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '采购订单更新失败', 'error': str(e)}), 400

# 删除采购订单
@bp.route('/<int:id>', methods=['DELETE'])
@require_permission('purchase:delete')
def delete_purchase_order(id):
    try:
        # 删除采购订单物品
        PurchaseOrderItem.query.filter_by(purchase_order_id=id).delete()
        # 删除采购订单
        order = PurchaseOrder.query.get(id)
        if not order:
            return jsonify({'message': '采购订单不存在'}), 404
        
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': '采购订单删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '采购订单删除失败', 'error': str(e)}), 400

# 采购订单详情
@bp.route('/<int:id>', methods=['GET'])
@require_permission('purchase:view')
def get_purchase_order_detail(id):
    try:
        order = PurchaseOrder.query.get(id)
        if not order:
            return jsonify({'message': '采购订单不存在'}), 404
        
        return jsonify(order.to_dict())
    except Exception as e:
        return jsonify({'message': '获取采购订单详情失败', 'error': str(e)}), 400
