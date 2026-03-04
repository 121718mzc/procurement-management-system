# 应用入口文件
from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.config import Config
from db import db

# 创建Flask应用实例
app = Flask(__name__)

# 加载配置
app.config.from_object(Config)

# 启用CORS
CORS(app)

# 初始化数据库
with app.app_context():
    db.init_app(app)

# 导入模型
from models.supplier import Supplier
from models.material import Material
from models.pricing import Pricing
from models.contract import Contract
from models.contract_item import ContractItem
from models.purchase_order import PurchaseOrder
from models.purchase_order_item import PurchaseOrderItem
from models.user import User

# 导入路由
from routes.supplier import bp as supplier_bp
from routes.material import bp as material_bp
from routes.pricing import bp as pricing_bp
from routes.contract import bp as contract_bp
from routes.purchase import bp as purchase_bp
from routes.user import bp as user_bp

# 注册蓝图
app.register_blueprint(supplier_bp)
app.register_blueprint(material_bp)
app.register_blueprint(pricing_bp)
app.register_blueprint(contract_bp)
app.register_blueprint(purchase_bp)
app.register_blueprint(user_bp)

# 初始化数据库
try:
    with app.app_context():
        # 直接创建表
        db.create_all()
    print("Database initialized successfully")
except Exception as e:
    print(f"Error initializing database: {e}")

# 测试路由
@app.route('/test')
def test():
    return jsonify({'message': 'Test route works!'})

if __name__ == '__main__':
    app.run(debug=True)
