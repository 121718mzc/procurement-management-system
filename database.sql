-- 采购管理系统数据库脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS procurement_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE procurement_db;

-- 创建物料分类表
CREATE TABLE IF NOT EXISTS material_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建供应商表
CREATE TABLE IF NOT EXISTS suppliers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100) UNIQUE,
    address VARCHAR(255),
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建物料表
CREATE TABLE IF NOT EXISTS materials (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    specification VARCHAR(255),
    unit VARCHAR(20) NOT NULL,
    category_id INT,
    stock DECIMAL(10,2) DEFAULT 0,
    min_stock DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES material_categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建价格表
CREATE TABLE IF NOT EXISTS pricings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_id INT,
    material_id INT,
    price DECIMAL(10,2) NOT NULL,
    effective_date DATE NOT NULL,
    expiry_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (material_id) REFERENCES materials(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建合同类型表
CREATE TABLE IF NOT EXISTS contract_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建合同表
CREATE TABLE IF NOT EXISTS contracts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_id INT,
    contract_number VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建合同物品表
CREATE TABLE IF NOT EXISTS contract_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT,
    material_id INT,
    quantity DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES contracts(id),
    FOREIGN KEY (material_id) REFERENCES materials(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建采购订单表
CREATE TABLE IF NOT EXISTS purchase_orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    contract_id INT,
    supplier_id INT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    order_date DATE NOT NULL,
    delivery_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (contract_id) REFERENCES contracts(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建采购订单物品表
CREATE TABLE IF NOT EXISTS purchase_order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    purchase_order_id INT,
    material_id INT,
    quantity DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders(id),
    FOREIGN KEY (material_id) REFERENCES materials(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入初始数据

-- 插入物料分类
INSERT INTO material_categories (name, description) VALUES
('生产原料', '用于生产过程的原材料'),
('电子元件', '电子类零部件'),
('包装材料', '产品包装所需材料'),
('办公耗材', '办公室日常使用的耗材');

-- 插入合同类型
INSERT INTO contract_types (name, description) VALUES
('NDA保密协议', '保密协议，保护商业机密'),
('多物品采购合同', '包含多种物料的采购合同');

-- 插入用户（密码：123456，已加密）
INSERT INTO users (username, password, name, phone, email) VALUES
('buyer', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', '采购员', '13800138000', 'buyer@example.com');

-- 插入供应商
INSERT INTO suppliers (name, contact_person, phone, email, address) VALUES
('供应商A', '张三', '13900139001', 'contact@supplierA.com', '北京市朝阳区'),
('供应商B', '李四', '13900139002', 'contact@supplierB.com', '上海市浦东新区');

-- 插入物料
INSERT INTO materials (code, name, specification, unit, category_id) VALUES
('MAT001', 'CPU', 'Intel i7', '个', 2),
('MAT002', '内存', '8GB DDR4', '条', 2),
('MAT003', '硬盘', '1TB SSD', '个', 2),
('MAT004', '纸箱', '30x20x20cm', '个', 3),
('MAT005', 'A4纸', '80g', '包', 4);

-- 插入价格
INSERT INTO pricings (supplier_id, material_id, price, effective_date) VALUES
(1, 1, 2000.00, '2026-01-01'),
(1, 2, 300.00, '2026-01-01'),
(2, 1, 1950.00, '2026-01-01'),
(2, 3, 500.00, '2026-01-01');

-- 插入合同
INSERT INTO contracts (supplier_id, contract_number, type, title, content, start_date, end_date, status) VALUES
(1, 'CON2026001', 'NDA', '2026年采购合同', '本合同为2026年度采购合同，包含CPU、内存等物料', '2026-01-01', '2026-12-31', 'active');

-- 插入合同物品
INSERT INTO contract_items (contract_id, material_id, quantity, unit_price, total_price) VALUES
(1, 1, 100.00, 2000.00, 200000.00),
(1, 2, 200.00, 300.00, 60000.00);

-- 插入采购订单
INSERT INTO purchase_orders (contract_id, supplier_id, order_number, order_date, delivery_date, status) VALUES
(1, 1, 'PO2026001', '2026-01-10', '2026-01-20', 'completed');

-- 插入采购订单物品
INSERT INTO purchase_order_items (purchase_order_id, material_id, quantity, unit_price, total_price, status) VALUES
(1, 1, 10.00, 2000.00, 20000.00, 'pending'),
(1, 2, 20.00, 300.00, 6000.00, 'pending');

-- 创建索引
CREATE INDEX idx_materials_category_id ON materials(category_id);
CREATE INDEX idx_pricings_supplier_id ON pricings(supplier_id);
CREATE INDEX idx_pricings_material_id ON pricings(material_id);
CREATE INDEX idx_contracts_supplier_id ON contracts(supplier_id);
CREATE INDEX idx_contract_items_contract_id ON contract_items(contract_id);
CREATE INDEX idx_contract_items_material_id ON contract_items(material_id);
CREATE INDEX idx_purchase_orders_supplier_id ON purchase_orders(supplier_id);
CREATE INDEX idx_purchase_orders_contract_id ON purchase_orders(contract_id);
CREATE INDEX idx_purchase_order_items_purchase_order_id ON purchase_order_items(purchase_order_id);
CREATE INDEX idx_purchase_order_items_material_id ON purchase_order_items(material_id);
