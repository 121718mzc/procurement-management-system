# 物料路由
from flask import Blueprint, request, jsonify
from models.material import Material
from models.material_category import MaterialCategory
from db import db

# 创建蓝图
bp = Blueprint('material', __name__, url_prefix='/material')

# 物料列表
@bp.route('/', methods=['GET'])
def get_materials():
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 分页查询
        materials = Material.query.paginate(page=page, per_page=per_page, error_out=False)
        
        # 构建响应
        result = []
        for material in materials.items:
            result.append(material.to_dict())
        
        return jsonify({
            'data': result,
            'total': materials.total,
            'page': materials.page,
            'per_page': materials.per_page,
            'pages': materials.pages
        })
    except Exception as e:
        print(f"Error in get_materials: {e}")
        return jsonify({'message': '获取物料列表失败', 'error': str(e)}), 500

# 添加物料
@bp.route('/', methods=['POST'])
def add_material():
    data = request.json
    try:
        material = Material(
            code=data['code'],
            name=data['name'],
            specification=data['specification'],
            category_id=data['category_id'],
            unit=data['unit'],
            stock=data.get('stock', 0),
            min_stock=data.get('min_stock', 0),
            status=data.get('status', 'active')
        )
        db.session.add(material)
        db.session.commit()
        return jsonify({'message': '物料添加成功', 'data': material.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '物料添加失败', 'error': str(e)}), 400

# 编辑物料
@bp.route('/<int:id>', methods=['PUT'])
def update_material(id):
    data = request.json
    try:
        material = Material.query.get(id)
        if not material:
            return jsonify({'message': '物料不存在'}), 404
        
        material.code = data.get('code', material.code)
        material.name = data.get('name', material.name)
        material.specification = data.get('specification', material.specification)
        material.category_id = data.get('category_id', material.category_id)
        material.unit = data.get('unit', material.unit)
        material.stock = data.get('stock', material.stock)
        material.min_stock = data.get('min_stock', material.min_stock)
        material.status = data.get('status', material.status)
        
        db.session.commit()
        return jsonify({'message': '物料更新成功', 'data': material.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '物料更新失败', 'error': str(e)}), 400

# 删除物料
@bp.route('/<int:id>', methods=['DELETE'])
def delete_material(id):
    try:
        material = Material.query.get(id)
        if not material:
            return jsonify({'message': '物料不存在'}), 404
        
        db.session.delete(material)
        db.session.commit()
        return jsonify({'message': '物料删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '物料删除失败', 'error': str(e)}), 400

# 物料分类
@bp.route('/categories', methods=['GET'])
def get_categories():
    categories = MaterialCategory.query.all()
    return jsonify([category.to_dict() for category in categories])

# 添加物料分类
@bp.route('/categories', methods=['POST'])
def add_category():
    data = request.json
    try:
        category = MaterialCategory(
            name=data['name'],
            description=data.get('description', '')
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({'message': '物料分类添加成功', 'data': category.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '物料分类添加失败', 'error': str(e)}), 400
