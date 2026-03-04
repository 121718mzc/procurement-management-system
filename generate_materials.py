# 批量生成物料数据脚本
import sys
import os

# 添加后端目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'procurement-backend'))

from app import app, db
from models.material import Material
from faker import Faker
import random

# 初始化Faker
fake = Faker('zh_CN')

def generate_materials(count=10):
    """生成指定数量的物料数据"""
    materials = []
    for i in range(count):
        material = Material(
            code=fake.bothify('MAT-###'),
            name=fake.word(),
            specification=fake.paragraph(nb_sentences=1),
            description=fake.paragraph(nb_sentences=2),
            category_id=random.randint(1, 4),
            supplier_id=random.randint(1, 10),
            unit=random.choice(['个', '条', '件', '箱', '套']),
            stock=random.randint(0, 1000),
            min_stock=random.randint(0, 100)
        )
        materials.append(material)
    return materials

if __name__ == '__main__':
    with app.app_context():
        # 生成20个物料数据
        materials = generate_materials(20)
        
        # 批量添加到数据库
        db.session.add_all(materials)
        
        # 提交事务
        db.session.commit()
        
        print(f"成功生成 {len(materials)} 个物料数据")
