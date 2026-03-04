#!/usr/bin/env python3
# 生成采购订单测试数据
import random
from datetime import datetime, timedelta
import mysql.connector

# 数据库连接信息
config = {
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'database': 'procurement_db',
    'raise_on_warnings': True
}

# 连接数据库
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# 生成采购订单数据
def generate_purchase_orders():
    # 供应商ID列表（假设供应商表已有数据）
    supplier_ids = [1, 2, 3, 4, 5]
    
    # 状态列表
    statuses = ['draft', 'sent', 'received', 'completed', 'cancelled']
    
    # 生成10条采购订单数据
    for i in range(1, 11):
        # 生成订单编号
        order_number = f'PO-2026-{i:03d}'
        
        # 随机选择供应商
        supplier_id = random.choice(supplier_ids)
        
        # 生成订单日期（最近30天内）
        order_date = datetime.now() - timedelta(days=random.randint(0, 30))
        order_date_str = order_date.strftime('%Y-%m-%d')
        
        # 生成预计交付日期（订单日期后1-30天）
        expected_delivery_date = order_date + timedelta(days=random.randint(1, 30))
        expected_delivery_date_str = expected_delivery_date.strftime('%Y-%m-%d')
        
        # 生成总金额（1000-10000之间）
        total_amount = round(random.uniform(1000, 10000), 2)
        
        # 随机选择状态
        status = random.choice(statuses)
        
        # 插入采购订单数据
        add_order = ("INSERT INTO purchase_orders "
                    "(supplier_id, order_number, order_date, expected_delivery_date, total_amount, status) "
                    "VALUES (%s, %s, %s, %s, %s, %s)")
        order_data = (supplier_id, order_number, order_date_str, expected_delivery_date_str, total_amount, status)
        cursor.execute(add_order, order_data)
        
        # 获取刚插入的采购订单ID
        order_id = cursor.lastrowid
        
        # 为每个采购订单生成1-3个物品
        item_count = random.randint(1, 3)
        for j in range(item_count):
            # 随机选择物料ID（假设物料表已有数据）
            material_id = random.randint(1, 10)
            
            # 生成数量（1-100）
            quantity = random.randint(1, 100)
            
            # 生成单价（10-1000）
            unit_price = round(random.uniform(10, 1000), 2)
            
            # 计算总价
            total_price = round(quantity * unit_price, 2)
            
            # 插入采购订单物品数据
            add_item = ("INSERT INTO purchase_order_items "
                       "(purchase_order_id, material_id, quantity, unit_price, total_price) "
                       "VALUES (%s, %s, %s, %s, %s)")
            item_data = (order_id, material_id, quantity, unit_price, total_price)
            cursor.execute(add_item, item_data)
    
    # 提交事务
    cnx.commit()
    print("采购订单测试数据生成完成！")

# 执行生成函数
try:
    generate_purchase_orders()
except Exception as e:
    print(f"生成数据时出错: {e}")
    cnx.rollback()
finally:
    # 关闭连接
    cursor.close()
    cnx.close()