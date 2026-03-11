-- 添加contracts表的type_code字段（针对procurement_db数据库）
ALTER TABLE procurement_db.contracts ADD COLUMN type_code VARCHAR(20);

-- 更新现有数据的type_code值
UPDATE procurement_db.contracts SET type_code = 'NDA' WHERE type LIKE '%NDA%';
UPDATE procurement_db.contracts SET type_code = 'Purchase' WHERE type LIKE '%采购%';

-- 为type_code字段添加索引（可选）
CREATE INDEX idx_contracts_type_code ON procurement_db.contracts(type_code);

-- 查看更新结果
SELECT id, contract_number, type, type_code FROM procurement_db.contracts;