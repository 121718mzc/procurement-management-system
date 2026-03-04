# 采购管理系统业务模型关系图（带连接线和表字段）

## 业务实体关系图

```
+-------------------------------+       +-------------------------------------+       +-----------------------------------+
|  物料分类(MaterialCategory)    |<------|    物料(Material)                     |<------|    价格(Price)                       |
|-------------------------------|       |-------------------------------------|       |-----------------------------------|
| id (PK)                       |       | id (PK)                             |       | id (PK)                           |
| name                          |       | code                                |       | supplier_id (FK)                  |
| description                   |       | name                                |       | material_id (FK)                  |
| created_at                    |       | specification                       |       | price                             |
| updated_at                    |       | unit                                |       | effective_date                    |
|                               |       | category_id (FK)                    |       | expiry_date                       |
|                               |       | stock                               |       | created_at                        |
|                               |       | min_stock                           |       | updated_at                        |
|                               |       | created_at                          |       |                                   |
|                               |       | updated_at                          |       |                                   |
+-------------------------------+       +-------------------------------------+       +-----------------------------------+
                                                      ^                                           ^
                                                      |                                           |
                                                      v                                           v
+-------------------------------+       +-------------------------------------+       +-----------------------------------+
|  合同类型(ContractType)         |<------|    合同(Contract)                      |<------| 采购订单(PurchaseOrder)              |
|-------------------------------|       |-------------------------------------|       |-----------------------------------|
| id (PK)                       |       | id (PK)                             |       | id (PK)                           |
| name                          |       | contract_number                      |       | order_number                      |
| description                   |       | type_id (FK)                        |       | supplier_id (FK)                  |
| created_at                    |       | supplier_id (FK)                    |       | contract_id (FK)                  |
| updated_at                    |       | title                               |       | status                            |
|                               |       | content                             |       | created_by (FK)                   |
|                               |       | start_date                          |       | created_at                        |
|                               |       | end_date                            |       | updated_at                        |
|                               |       | status                              |       |                                   |
|                               |       | created_by (FK)                     |       |                                   |
|                               |       | created_at                          |       |                                   |
|                               |       | updated_at                          |       |                                   |
+-------------------------------+       +-------------------------------------+       +-----------------------------------+
                                                      ^                                           ^
                                                      |                                           |
                                                      v                                           v
+-------------------------------+       +-------------------------------------+       +-----------------------------------+
|    供应商(Supplier)              |<------|  合同物品(ContractItem)                |<------|采购订单物品(PurchaseOrderItem)        |
|-------------------------------|       |-------------------------------------|       |-----------------------------------|
| id (PK)                       |       | id (PK)                             |       | id (PK)                           |
| name                          |       | contract_id (FK)                    |       | order_id (FK)                     |
| contact_person                |       | material_id (FK)                    |       | material_id (FK)                  |
| phone                         |       | quantity                            |       | quantity                          |
| email                         |       | unit_price                          |       | unit_price                        |
| address                       |       | total_price                         |       | total_price                       |
| status                        |       | created_at                          |       | created_at                        |
| created_at                    |       | updated_at                          |       | updated_at                        |
| updated_at                    |       |                                     |       |                                   |
+-------------------------------+       +-------------------------------------+       +-----------------------------------+
                                                      ^
                                                      |
                                                      v
+-------------------------------+       +-------------------------------------+
|    用户(User)                    |<------|    合同(Contract)                      |
|-------------------------------|       |-------------------------------------|
| id (PK)                       |       | id (PK)                             |
| username                      |       | contract_number                      |
| password                      |       | type_id (FK)                        |
| name                          |       | supplier_id (FK)                    |
| phone                         |       | title                               |
| email                         |       | content                             |
| status                        |       | start_date                          |
| created_at                    |       | end_date                            |
| updated_at                    |       | status                              |
|                               |       | created_by (FK)                     |
|                               |       | created_at                          |
|                               |       | updated_at                          |
+-------------------------------+       +-------------------------------------+
                                                      ^
                                                      |
                                                      v
                                            +-------------------------------------+
                                            | 采购订单(PurchaseOrder)              |
                                            |-------------------------------------|
                                            | id (PK)                             |
                                            | order_number                        |
                                            | supplier_id (FK)                    |
                                            | contract_id (FK)                    |
                                            | status                              |
                                            | created_by (FK)                     |
                                            | created_at                          |
                                            | updated_at                          |
                                            +-------------------------------------+
```

## 详细业务关系说明

### 1. 物料分类与物料
- **关系**：一对多
- **连接字段**：`materials.category_id` → `material_categories.id`
- **业务描述**：物料分类是对物料的归类，一个物料分类可以包含多个物料，每个物料必须属于一个物料分类

### 2. 物料与价格
- **关系**：一对多
- **连接字段**：`pricing.material_id` → `materials.id`
- **业务描述**：物料的价格由供应商提供，一个物料可以有多个价格（不同供应商或不同时期），每个价格对应一个物料

### 3. 供应商与价格
- **关系**：一对多
- **连接字段**：`pricing.supplier_id` → `suppliers.id`
- **业务描述**：供应商为物料提供价格，一个供应商可以提供多个物料的价格，每个价格对应一个供应商

### 4. 合同类型与合同
- **关系**：一对多
- **连接字段**：`contracts.type_id` → `contract_types.id`
- **业务描述**：合同类型定义了合同的性质，一个合同类型可以对应多个合同，每个合同属于一个合同类型

### 5. 供应商与合同
- **关系**：一对多
- **连接字段**：`contracts.supplier_id` → `suppliers.id`
- **业务描述**：合同是与供应商签订的，一个供应商可以签订多个合同，每个合同对应一个供应商

### 6. 用户与合同
- **关系**：一对多
- **连接字段**：`contracts.created_by` → `users.id`
- **业务描述**：合同由用户创建，一个用户可以创建多个合同，每个合同由一个用户创建

### 7. 合同与合同物品
- **关系**：一对多
- **连接字段**：`contract_items.contract_id` → `contracts.id`
- **业务描述**：合同包含具体的采购物品，一个合同可以包含多个物品，每个物品属于一个合同

### 8. 物料与合同物品
- **关系**：一对多
- **连接字段**：`contract_items.material_id` → `materials.id`
- **业务描述**：合同物品是具体的物料，一个物料可以出现在多个合同物品中，每个合同物品对应一个物料

### 9. 供应商与采购订单
- **关系**：一对多
- **连接字段**：`purchase_orders.supplier_id` → `suppliers.id`
- **业务描述**：采购订单发送给供应商，一个供应商可以接收多个采购订单，每个采购订单对应一个供应商

### 10. 合同与采购订单
- **关系**：一对多
- **连接字段**：`purchase_orders.contract_id` → `contracts.id`
- **业务描述**：采购订单基于合同创建，一个合同可以对应多个采购订单，每个采购订单对应一个合同

### 11. 用户与采购订单
- **关系**：一对多
- **连接字段**：`purchase_orders.created_by` → `users.id`
- **业务描述**：采购订单由用户创建，一个用户可以创建多个采购订单，每个采购订单由一个用户创建

### 12. 采购订单与采购订单物品
- **关系**：一对多
- **连接字段**：`purchase_order_items.order_id` → `purchase_orders.id`
- **业务描述**：采购订单包含具体的采购物品，一个采购订单可以包含多个物品，每个物品属于一个采购订单

### 13. 物料与采购订单物品
- **关系**：一对多
- **连接字段**：`purchase_order_items.material_id` → `materials.id`
- **业务描述**：采购订单物品是具体的物料，一个物料可以出现在多个采购订单物品中，每个采购订单物品对应一个物料

## 业务实体字段说明

### 1. 物料分类(MaterialCategory)
- **id**：分类ID，主键
- **name**：分类名称，必填
- **description**：分类描述
- **created_at**：创建时间
- **updated_at**：更新时间

### 2. 物料(Material)
- **id**：物料ID，主键
- **code**：物料编码，唯一，必填
- **name**：物料名称，必填
- **specification**：规格型号
- **unit**：单位，必填
- **category_id**：分类ID，外键
- **stock**：库存数量，默认0
- **min_stock**：最低库存，默认0
- **created_at**：创建时间
- **updated_at**：更新时间

### 3. 供应商(Supplier)
- **id**：供应商ID，主键
- **name**：供应商名称，必填
- **contact_person**：联系人，必填
- **phone**：联系电话，必填
- **email**：邮箱，唯一
- **address**：地址
- **status**：状态，枚举(active, inactive)，默认active
- **created_at**：创建时间
- **updated_at**：更新时间

### 4. 价格(Price)
- **id**：价格ID，主键
- **supplier_id**：供应商ID，外键
- **material_id**：物料ID，外键
- **price**：价格，必填
- **effective_date**：生效日期，必填
- **expiry_date**：过期日期
- **created_at**：创建时间
- **updated_at**：更新时间

### 5. 合同类型(ContractType)
- **id**：类型ID，主键
- **name**：类型名称，必填
- **description**：类型描述
- **created_at**：创建时间
- **updated_at**：更新时间

### 6. 合同(Contract)
- **id**：合同ID，主键
- **contract_number**：合同编号，唯一，必填
- **type_id**：合同类型ID，外键
- **supplier_id**：供应商ID，外键
- **title**：合同标题，必填
- **content**：合同内容，必填
- **start_date**：开始日期，必填
- **end_date**：结束日期
- **status**：状态，枚举(draft, signed, expired)，默认draft
- **created_by**：创建人ID，外键
- **created_at**：创建时间
- **updated_at**：更新时间

### 7. 合同物品(ContractItem)
- **id**：物品ID，主键
- **contract_id**：合同ID，外键
- **material_id**：物料ID，外键
- **quantity**：数量，必填
- **unit_price**：单价，必填
- **total_price**：总价，必填
- **created_at**：创建时间
- **updated_at**：更新时间

### 8. 采购订单(PurchaseOrder)
- **id**：订单ID，主键
- **order_number**：订单编号，唯一，必填
- **supplier_id**：供应商ID，外键
- **contract_id**：合同ID，外键
- **status**：状态，枚举(draft, sent, received, completed, cancelled)，默认draft
- **created_by**：创建人ID，外键
- **created_at**：创建时间
- **updated_at**：更新时间

### 9. 采购订单物品(PurchaseOrderItem)
- **id**：物品ID，主键
- **order_id**：订单ID，外键
- **material_id**：物料ID，外键
- **quantity**：数量，必填
- **unit_price**：单价，必填
- **total_price**：总价，必填
- **created_at**：创建时间
- **updated_at**：更新时间

### 10. 用户(User)
- **id**：用户ID，主键
- **username**：用户名，唯一，必填
- **password**：密码，必填
- **name**：姓名，必填
- **phone**：电话
- **email**：邮箱，唯一
- **status**：状态，枚举(active, inactive)，默认active
- **created_at**：创建时间
- **updated_at**：更新时间

## 业务流程关系

### 1. 采购流程
1. **需求确认**：确定需要采购的物料和数量
2. **供应商选择**：根据物料和价格选择合适的供应商
3. **合同签订**：与供应商签订采购合同
4. **订单创建**：基于合同创建采购订单
5. **订单执行**：供应商发货，企业验收
6. **订单完成**：确认收货，完成采购流程

### 2. 合同管理流程
1. **合同起草**：创建合同草稿，填写合同内容
2. **合同审核**：审核合同内容
3. **合同签署**：与供应商签署合同
4. **合同执行**：根据合同条款执行采购
5. **合同归档**：合同到期后归档

### 3. 物料管理流程
1. **物料分类**：建立物料分类体系
2. **物料录入**：录入物料基本信息
3. **库存管理**：监控物料库存状态
4. **价格管理**：管理物料价格信息
5. **物料使用**：在采购订单中使用物料

## 业务模型特点

1. **完整性**：覆盖了采购管理的完整业务流程
2. **清晰性**：业务实体之间的关系明确清晰
3. **可扩展性**：支持业务流程的扩展和变更
4. **实用性**：直接对应实际业务操作
5. **一致性**：与数据库模型保持一致

## 使用说明

1. **业务分析**：使用此关系图进行业务需求分析和系统设计
2. **流程优化**：基于业务流程关系，优化采购管理流程
3. **系统开发**：作为系统开发的业务模型基础
4. **用户培训**：用于培训用户理解系统的业务逻辑
5. **业务扩展**：当业务需求变更时，可基于此模型进行扩展

此业务模型关系图详细描述了采购管理系统的业务实体、字段和流程，为系统开发和业务运营提供了清晰的指导。