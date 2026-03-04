# 采购订单模型
from db import db

class PurchaseOrder(db.Model):
    __tablename__ = 'purchase_orders'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    order_number = db.Column(db.String(50), nullable=False, unique=True)
    order_date = db.Column(db.Date, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # 关系
    items = db.relationship('PurchaseOrderItem', backref='purchase_order', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'contract_id': self.contract_id,
            'contract_name': self.contract.title if hasattr(self, 'contract') else None,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier.name if hasattr(self, 'supplier') else None,
            'order_number': self.order_number,
            'order_date': self.order_date.strftime('%Y-%m-%d') if self.order_date else None,
            'delivery_date': self.delivery_date.strftime('%Y-%m-%d') if self.delivery_date else None,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'items': [item.to_dict() for item in self.items] if self.items else []
        }
