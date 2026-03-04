# 合同路由
from flask import Blueprint, request, jsonify, send_file
from models.contract import Contract
from models.contract_item import ContractItem
from db import db
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# 创建蓝图
bp = Blueprint('contract', __name__, url_prefix='/contract')

# 合同列表
@bp.route('/', methods=['GET'])
def get_contracts():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 分页查询
        contracts = Contract.query.paginate(page=page, per_page=per_page, error_out=False)
        
        # 构建响应
        result = []
        for contract in contracts.items:
            result.append(contract.to_dict())
        
        return jsonify({
            'data': result,
            'total': contracts.total,
            'page': contracts.page,
            'per_page': contracts.per_page,
            'pages': contracts.pages
        })
    except Exception as e:
        print(f"Error in get_contracts: {e}")
        return jsonify({'message': '获取合同列表失败', 'error': str(e)}), 500

# 添加合同
@bp.route('/', methods=['POST'])
def add_contract():
    data = request.json
    try:
        # 创建合同
        contract = Contract(
            supplier_id=data['supplier_id'],
            contract_number=data['contract_number'],
            type=data['type_name'],  # 使用type_name作为type字段
            title=data['title'],
            content=data['content'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            status=data.get('status', 'signed')
        )
        db.session.add(contract)
        db.session.flush()  # 获取contract.id
        
        # 添加合同物品
        if 'items' in data:
            for item in data['items']:
                contract_item = ContractItem(
                    contract_id=contract.id,
                    material_id=item['material_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    total_price=item['total_price']
                )
                db.session.add(contract_item)
        
        db.session.commit()
        return jsonify({'message': '合同添加成功', 'data': contract.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '合同添加失败', 'error': str(e)}), 400

# 编辑合同
@bp.route('/<int:id>', methods=['PUT'])
def update_contract(id):
    data = request.json
    try:
        contract = Contract.query.get(id)
        if not contract:
            return jsonify({'message': '合同不存在'}), 404
        
        # 更新合同信息
        contract.supplier_id = data.get('supplier_id', contract.supplier_id)
        contract.contract_number = data.get('contract_number', contract.contract_number)
        contract.type = data.get('type_name', contract.type)  # 使用type_name作为type字段
        contract.title = data.get('title', contract.title)
        contract.content = data.get('content', contract.content)
        contract.start_date = data.get('start_date', contract.start_date)
        contract.end_date = data.get('end_date', contract.end_date)
        contract.status = data.get('status', contract.status)
        
        # 更新合同物品
        if 'items' in data:
            # 删除旧物品
            ContractItem.query.filter_by(contract_id=id).delete()
            # 添加新物品
            for item in data['items']:
                contract_item = ContractItem(
                    contract_id=contract.id,
                    material_id=item['material_id'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    total_price=item['total_price']
                )
                db.session.add(contract_item)
        
        db.session.commit()
        return jsonify({'message': '合同更新成功', 'data': contract.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '合同更新失败', 'error': str(e)}), 400

# 删除合同
@bp.route('/<int:id>', methods=['DELETE'])
def delete_contract(id):
    try:
        # 删除合同物品
        ContractItem.query.filter_by(contract_id=id).delete()
        # 删除合同
        contract = Contract.query.get(id)
        if not contract:
            return jsonify({'message': '合同不存在'}), 404
        
        db.session.delete(contract)
        db.session.commit()
        return jsonify({'message': '合同删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '合同删除失败', 'error': str(e)}), 400

# 导出合同PDF
@bp.route('/<int:id>/export', methods=['GET'])
def export_contract(id):
    try:
        contract = Contract.query.get(id)
        if not contract:
            return jsonify({'message': '合同不存在'}), 404
        
        # 创建PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        
        # 标题
        p.setFont('Helvetica-Bold', 16)
        p.drawString(100, height - 50, contract.title)
        
        # 合同编号
        p.setFont('Helvetica', 12)
        p.drawString(100, height - 80, f'合同编号: {contract.contract_number}')
        
        # 供应商信息
        p.drawString(100, height - 100, f'供应商: {contract.supplier.name if hasattr(contract, "supplier") else "未知"}')
        
        # 合同类型
        p.drawString(100, height - 120, f'合同类型: {contract.type}')
        
        # 合同期限
        p.drawString(100, height - 140, f'开始日期: {contract.start_date.strftime("%Y-%m-%d") if contract.start_date else "未知"}')
        p.drawString(100, height - 160, f'结束日期: {contract.end_date.strftime("%Y-%m-%d") if contract.end_date else "未知"}')
        
        # 合同内容
        p.drawString(100, height - 200, '合同内容:')
        content_lines = contract.content.split('\n')
        y = height - 220
        for line in content_lines:
            p.drawString(120, y, line)
            y -= 20
        
        # 合同物品（如果有）
        items = ContractItem.query.filter_by(contract_id=id).all()
        if items:
            y -= 40
            p.drawString(100, y, '采购物品:')
            y -= 20
            p.drawString(120, y, '物料名称')
            p.drawString(300, y, '数量')
            p.drawString(380, y, '单价')
            p.drawString(460, y, '总价')
            y -= 20
            
            for item in items:
                material_name = item.material.name if hasattr(item, "material") else "未知"
                p.drawString(120, y, material_name)
                p.drawString(300, y, str(item.quantity))
                p.drawString(380, y, str(item.unit_price))
                p.drawString(460, y, str(item.total_price))
                y -= 20
        
        p.showPage()
        p.save()
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True, download_name=f'contract-{contract.contract_number}.pdf', mimetype='application/pdf')
    except Exception as e:
        return jsonify({'message': '合同PDF导出失败', 'error': str(e)}), 400
