-- 添加contracts表的type_code字段
ALTER TABLE contracts ADD COLUMN type_code VARCHAR(20);

-- 更新现有数据的type_code值
UPDATE contracts SET type_code = 'NDA' WHERE type LIKE '%NDA%';
UPDATE contracts SET type_code = 'Purchase' WHERE type LIKE '%采购%';

-- 为type_code字段添加索引（可选）
CREATE INDEX idx_contracts_type_code ON contracts(type_code);

-- 查看更新结果
SELECT id, contract_number, type, type_code FROM contracts;
