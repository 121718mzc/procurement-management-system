# 初始化物料分类数据
from app import app, db
from models.material_category import MaterialCategory

with app.app_context():
    # 创建表
    db.create_all()
    
    # 检查是否已有数据
    if not MaterialCategory.query.first():
        # 添加初始数据
        categories = [
            MaterialCategory(name='生产原料', description='用于生产的原材料'),
            MaterialCategory(name='电子元件', description='电子设备的零部件'),
            MaterialCategory(name='包装材料', description='用于包装产品的材料'),
            MaterialCategory(name='办公耗材', description='办公室使用的消耗品')
        ]
        for category in categories:
            db.session.add(category)
        db.session.commit()
        print('物料分类数据已初始化')
    else:
        print('物料分类数据已存在')