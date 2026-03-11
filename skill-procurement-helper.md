# 采购管理系统问题修复技能文档

## 问题描述

### 1. 合同管理模块错误
**错误信息**：
```
Error in get_contracts: (MySQLdb.OperationalError) (1054, "Unknown column 'contracts.type_code' in 'field list'")
[SQL: SELECT contracts.id AS contracts_id, contracts.supplier_id AS contracts_supplier_id, contracts.contract_number AS contracts_contract_number, contracts.type AS contracts_type, contracts.type_code AS contracts_type_code, contracts.title AS contracts_title, contracts.content AS contracts_content, contracts.start_date AS contracts_start_date, contracts.end_date AS contracts_end_date, contracts.status AS contracts_status, contracts.created_at AS contracts_created_at, contracts.updated_at AS contracts_updated_at
FROM contracts
 LIMIT %s, %s]
[parameters: (0, 10)]
```

**原因**：在`Contract`模型中添加了`type_code`字段，但是数据库表中还没有创建该字段。

### 2. 采购订单模块错误
**问题**：状态值不统一，后端使用`'pending'`状态，前端下拉选项中没有对应的选项。

### 3. 页面无法显示数据问题
**问题**：合同管理和采购订单页面无法显示数据，前端页面加载后无数据展示。

**原因**：
- 合同管理：数据库缺少`type_code`字段导致API调用失败
- 采购订单：可能存在类似的字段不匹配问题或状态值处理问题

## 解决方案

### 1. 合同管理模块修复

**步骤1：添加数据库字段**
执行以下SQL语句（针对procurement_db数据库）：

```sql
-- 添加contracts表的type_code字段（针对procurement_db数据库）
ALTER TABLE procurement_db.contracts ADD COLUMN type_code VARCHAR(20);

-- 更新现有数据的type_code值
UPDATE procurement_db.contracts SET type_code = 'NDA' WHERE type LIKE '%NDA%';
UPDATE procurement_db.contracts SET type_code = 'Purchase' WHERE type LIKE '%采购%';

-- 为type_code字段添加索引（可选）
CREATE INDEX idx_contracts_type_code ON procurement_db.contracts(type_code);

-- 查看更新结果
SELECT id, contract_number, type, type_code FROM procurement_db.contracts;
```

**步骤2：修改后端代码**
1. **更新Contract模型** (`procurement-backend/models/contract.py`)：
   - 添加`type_code`字段
   - 更新`to_dict`方法，包含`type_code`字段

2. **更新合同路由** (`procurement-backend/routes/contract.py`)：
   - 在添加和更新合同时处理`type_code`字段

**步骤3：修改前端代码**
1. **更新Contract.vue**：
   - 修改`getContracts`方法，使用后端返回的`type_code`字段
   - 更新`handleSubmit`方法，提交`type_code`字段

### 2. 采购订单模块修复

**步骤1：更新前端状态处理**
1. **更新Purchase.vue**：
   - 在`getStatusText`方法中添加对`'pending'`状态的处理
   - 在`getTagType`方法中添加对`'pending'`状态的处理
   - 在搜索表单和对话框中添加"待处理"状态选项

## 技术细节

### 合同类型字段映射
- **后端**：`type`字段存储类型名称，`type_code`字段存储类型代码
- **前端**：使用`type_code`字段进行类型映射，显示类型名称

### 状态值统一
- **后端**：支持`'pending'`、`'draft'`、`'sent'`、`'received'`、`'completed'`、`'cancelled'`状态
- **前端**：添加"待处理"选项，对应`'pending'`状态

## 测试验证

1. **运行前端测试**：
   ```bash
   npm test
   ```

2. **验证API调用**：
   - 访问合同管理页面，确保能够正常加载合同列表
   - 测试添加、编辑、删除合同功能
   - 测试采购订单的状态管理功能

3. **页面显示验证**：
   - 合同管理页面：确认数据能够正常显示，无加载错误
   - 采购订单页面：确认数据能够正常显示，状态选项完整
   - 验证所有API调用返回200状态码

4. **数据库验证**：
   - 确认`contracts`表中已添加`type_code`字段
   - 确认现有数据的`type_code`值已正确更新
   - 运行SQL查询验证数据完整性

## 相关文件

- **SQL文件**：`sql/add_contract_type_code_final.sql`
- **后端文件**：
  - `procurement-backend/models/contract.py`
  - `procurement-backend/routes/contract.py`
- **前端文件**：
  - `procurement-frontend/src/views/Contract.vue`
  - `procurement-frontend/src/views/Purchase.vue`

## 注意事项

1. **数据库迁移**：建议使用数据库迁移工具（如Flask-Migrate）管理数据库变更
2. **API兼容性**：确保前端和后端的字段名称和格式保持一致
3. **错误处理**：增强错误处理机制，提高系统的健壮性
4. **测试覆盖**：添加更多测试用例，确保功能的稳定性

## 解决方案验证

执行完上述步骤后，系统应该能够：
- 正常加载合同列表，无数据库错误
- 正确处理合同类型的显示和提交
- 采购订单的状态管理功能正常，包括"待处理"状态
- 所有测试用例通过验证
