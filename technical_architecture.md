# 采购管理系统技术架构文档

## 1. 系统架构概述

### 1.1 架构风格
本系统采用前后端分离的架构风格，前端使用Vue 3框架，后端使用Node.js + Express框架，数据库使用MySQL。

### 1.2 系统分层
- **前端层**：负责用户界面和交互逻辑
- **API层**：提供RESTful API接口
- **服务层**：实现业务逻辑
- **数据访问层**：负责数据库操作
- **数据存储层**：存储数据

## 2. 前端技术架构

### 2.1 技术栈
- **框架**：Vue 3
- **构建工具**：Vite
- **状态管理**：Pinia
- **路由**：Vue Router
- **UI组件库**：Element Plus
- **HTTP客户端**：Axios
- **PDF导出**：jsPDF

### 2.2 前端项目结构
```
├── public/              # 静态资源
├── src/
│   ├── assets/          # 资源文件
│   ├── components/      # 公共组件
│   ├── views/           # 页面组件
│   │   ├── supplier/    # 供应商管理
│   │   ├── material/    # 物料管理
│   │   ├── pricing/     # 定价管理
│   │   ├── contract/    # 合同管理
│   │   └── purchase/    # 采购管理
│   ├── router/          # 路由配置
│   ├── stores/          # Pinia状态管理
│   ├── services/        # API服务
│   ├── utils/           # 工具函数
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── .env                 # 环境变量
├── index.html           # HTML模板
├── package.json         # 项目配置
└── vite.config.js       # Vite配置
```

### 2.3 状态管理设计
使用Pinia进行状态管理，按模块划分store：
- **supplierStore**：供应商相关状态
- **materialStore**：物料相关状态
- **pricingStore**：定价相关状态
- **contractStore**：合同相关状态
- **purchaseStore**：采购相关状态
- **userStore**：用户相关状态

### 2.4 路由设计
```javascript
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/supplier',
    name: 'Supplier',
    component: SupplierView
  },
  {
    path: '/material',
    name: 'Material',
    component: MaterialView
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: PricingView
  },
  {
    path: '/contract',
    name: 'Contract',
    component: ContractView
  },
  {
    path: '/purchase',
    name: 'Purchase',
    component: PurchaseView
  }
]
```

## 3. 后端技术架构

### 3.1 技术栈
- **语言**：Python 3.9+
- **框架**：Flask 或 Django
- **数据库**：MySQL
- **ORM**：SQLAlchemy 或 Django ORM
- **认证**：简单的认证机制
- **PDF生成**：reportlab

### 3.2 后端项目结构
```
├── config/              # 配置文件
│   ├── __init__.py
│   └── config.py
├── controllers/         # 控制器
│   ├── __init__.py
│   ├── supplier.py      # 供应商控制器
│   ├── material.py      # 物料控制器
│   ├── pricing.py       # 定价控制器
│   ├── contract.py      # 合同控制器
│   ├── purchase.py      # 采购控制器
│   └── user.py          # 用户控制器
├── middleware/          # 中间件
│   ├── __init__.py
│   ├── auth.py          # 认证中间件
│   ├── error.py         # 错误处理中间件
│   └── validation.py    # 验证中间件
├── models/              # 数据模型
│   ├── __init__.py
│   ├── supplier.py      # 供应商模型
│   ├── material.py      # 物料模型
│   ├── material_category.py # 物料分类模型
│   ├── pricing.py       # 定价模型
│   ├── contract.py      # 合同模型
│   ├── contract_type.py  # 合同类型模型
│   ├── contract_item.py  # 合同物品模型
│   ├── purchase_order.py # 采购订单模型
│   ├── purchase_order_item.py # 采购订单物品模型
│   └── user.py          # 用户模型
├── routes/              # 路由
│   ├── __init__.py
│   ├── supplier.py      # 供应商路由
│   ├── material.py      # 物料路由
│   ├── pricing.py       # 定价路由
│   ├── contract.py      # 合同路由
│   ├── purchase.py      # 采购路由
│   └── user.py          # 用户路由
├── services/            # 业务逻辑
│   ├── __init__.py
│   ├── supplier.py      # 供应商服务
│   ├── material.py      # 物料服务
│   ├── pricing.py       # 定价服务
│   ├── contract.py      # 合同服务
│   ├── purchase.py      # 采购服务
│   └── user.py          # 用户服务
├── utils/               # 工具函数
│   ├── __init__.py
│   ├── pdf.py           # PDF生成工具
│   ├── validator.py     # 验证工具
│   └── response.py      # 响应工具
├── app.py               # 应用入口
├── requirements.txt     # 依赖配置
└── run.py               # 服务器启动
```

### 3.3 API设计

#### 3.3.1 供应商API
- `GET /api/suppliers` - 获取供应商列表
- `GET /api/suppliers/:id` - 获取供应商详情
- `POST /api/suppliers` - 创建供应商
- `PUT /api/suppliers/:id` - 更新供应商
- `DELETE /api/suppliers/:id` - 删除供应商

#### 3.3.2 物料API
- `GET /api/materials` - 获取物料列表
- `GET /api/materials/:id` - 获取物料详情
- `POST /api/materials` - 创建物料
- `PUT /api/materials/:id` - 更新物料
- `DELETE /api/materials/:id` - 删除物料
- `GET /api/material-categories` - 获取物料分类列表
- `POST /api/material-categories` - 创建物料分类
- `PUT /api/material-categories/:id` - 更新物料分类
- `DELETE /api/material-categories/:id` - 删除物料分类

#### 3.3.3 定价API
- `GET /api/pricing` - 获取价格列表
- `POST /api/pricing` - 创建价格
- `PUT /api/pricing/:id` - 更新价格
- `DELETE /api/pricing/:id` - 删除价格

#### 3.3.4 合同API
- `GET /api/contracts` - 获取合同列表
- `GET /api/contracts/:id` - 获取合同详情
- `POST /api/contracts` - 创建合同
- `PUT /api/contracts/:id` - 更新合同
- `DELETE /api/contracts/:id` - 删除合同
- `GET /api/contracts/:id/export` - 导出合同为PDF
- `GET /api/contract-types` - 获取合同类型列表

#### 3.3.5 采购API
- `GET /api/purchase-orders` - 获取采购订单列表
- `POST /api/purchase-orders` - 创建采购订单
- `PUT /api/purchase-orders/:id` - 更新采购订单
- `DELETE /api/purchase-orders/:id` - 删除采购订单

#### 3.3.6 用户API
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/profile` - 获取用户信息

## 4. 数据库设计

### 4.1 数据库表结构

#### 4.1.1 供应商表 (`suppliers`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 供应商ID |
| `name` | `VARCHAR(255)` | `NOT NULL` | 供应商名称 |
| `contact_person` | `VARCHAR(100)` | `NOT NULL` | 联系人 |
| `phone` | `VARCHAR(20)` | `NOT NULL` | 联系电话 |
| `email` | `VARCHAR(100)` | `UNIQUE` | 邮箱 |
| `address` | `VARCHAR(255)` | | 地址 |
| `status` | `ENUM('active', 'inactive')` | `DEFAULT 'active'` | 状态 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.2 物料分类表 (`material_categories`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 分类ID |
| `name` | `VARCHAR(100)` | `NOT NULL` | 分类名称 |
| `description` | `TEXT` | | 分类描述 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.3 物料表 (`materials`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 物料ID |
| `code` | `VARCHAR(50)` | `UNIQUE, NOT NULL` | 物料编码 |
| `name` | `VARCHAR(255)` | `NOT NULL` | 物料名称 |
| `specification` | `VARCHAR(255)` | | 规格型号 |
| `unit` | `VARCHAR(20)` | `NOT NULL` | 单位 |
| `category_id` | `INT` | `FOREIGN KEY REFERENCES material_categories(id)` | 分类ID |
| `stock` | `DECIMAL(10,2)` | `DEFAULT 0` | 库存数量 |
| `min_stock` | `DECIMAL(10,2)` | `DEFAULT 0` | 最低库存 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.4 用户表 (`users`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 用户ID |
| `username` | `VARCHAR(50)` | `UNIQUE, NOT NULL` | 用户名 |
| `password` | `VARCHAR(255)` | `NOT NULL` | 密码 |
| `name` | `VARCHAR(100)` | `NOT NULL` | 姓名 |
| `phone` | `VARCHAR(20)` | | 电话 |
| `email` | `VARCHAR(100)` | `UNIQUE` | 邮箱 |
| `status` | `ENUM('active', 'inactive')` | `DEFAULT 'active'` | 状态 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.5 价格表 (`pricing`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 价格ID |
| `supplier_id` | `INT` | `FOREIGN KEY REFERENCES suppliers(id)` | 供应商ID |
| `material_id` | `INT` | `FOREIGN KEY REFERENCES materials(id)` | 物料ID |
| `price` | `DECIMAL(10,2)` | `NOT NULL` | 价格 |
| `effective_date` | `DATE` | `NOT NULL` | 生效日期 |
| `expiry_date` | `DATE` | | 过期日期 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.6 合同类型表 (`contract_types`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 类型ID |
| `name` | `VARCHAR(100)` | `NOT NULL` | 类型名称 |
| `description` | `TEXT` | | 类型描述 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.7 合同表 (`contracts`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 合同ID |
| `contract_number` | `VARCHAR(50)` | `UNIQUE, NOT NULL` | 合同编号 |
| `type_id` | `INT` | `FOREIGN KEY REFERENCES contract_types(id)` | 合同类型ID |
| `supplier_id` | `INT` | `FOREIGN KEY REFERENCES suppliers(id)` | 供应商ID |
| `title` | `VARCHAR(255)` | `NOT NULL` | 合同标题 |
| `content` | `TEXT` | `NOT NULL` | 合同内容 |
| `start_date` | `DATE` | `NOT NULL` | 开始日期 |
| `end_date` | `DATE` | | 结束日期 |
| `status` | `ENUM('draft', 'signed', 'expired')` | `DEFAULT 'draft'` | 状态 |
| `created_by` | `INT` | `FOREIGN KEY REFERENCES users(id)` | 创建人 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.8 合同物品表 (`contract_items`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 物品ID |
| `contract_id` | `INT` | `FOREIGN KEY REFERENCES contracts(id)` | 合同ID |
| `material_id` | `INT` | `FOREIGN KEY REFERENCES materials(id)` | 物料ID |
| `quantity` | `DECIMAL(10,2)` | `NOT NULL` | 数量 |
| `unit_price` | `DECIMAL(10,2)` | `NOT NULL` | 单价 |
| `total_price` | `DECIMAL(10,2)` | `NOT NULL` | 总价 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.9 采购订单表 (`purchase_orders`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 订单ID |
| `order_number` | `VARCHAR(50)` | `UNIQUE, NOT NULL` | 订单编号 |
| `supplier_id` | `INT` | `FOREIGN KEY REFERENCES suppliers(id)` | 供应商ID |
| `contract_id` | `INT` | `FOREIGN KEY REFERENCES contracts(id)` | 合同ID |
| `status` | `ENUM('draft', 'sent', 'received', 'completed', 'cancelled')` | `DEFAULT 'draft'` | 状态 |
| `created_by` | `INT` | `FOREIGN KEY REFERENCES users(id)` | 创建人 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.10 采购订单物品表 (`purchase_order_items`)
| 字段名 | 数据类型 | 约束 | 描述 |
| --- | --- | --- | --- |
| `id` | `INT` | `PRIMARY KEY, AUTO_INCREMENT` | 物品ID |
| `order_id` | `INT` | `FOREIGN KEY REFERENCES purchase_orders(id)` | 订单ID |
| `material_id` | `INT` | `FOREIGN KEY REFERENCES materials(id)` | 物料ID |
| `quantity` | `DECIMAL(10,2)` | `NOT NULL` | 数量 |
| `unit_price` | `DECIMAL(10,2)` | `NOT NULL` | 单价 |
| `total_price` | `DECIMAL(10,2)` | `NOT NULL` | 总价 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | 更新时间 |

## 5. 系统安全

### 5.1 认证与授权
- 简单的用户认证机制
- 密码加密存储

### 5.2 数据安全
- 数据传输加密（HTTPS）
- 数据库访问控制
- 敏感数据加密存储

### 5.3 防攻击措施
- SQL注入防护
- XSS防护
- CSRF防护

## 6. 部署与集成

### 6.1 部署方案
- **前端**：部署到Nginx或Apache服务器
- **后端**：部署到Node.js服务器
- **数据库**：部署到MySQL服务器

## 7. 性能优化

### 7.1 前端优化
- 代码分割
- 资源压缩
- 缓存策略
- 懒加载

### 7.2 后端优化
- 数据库索引优化
- 查询优化
- 缓存机制

### 7.3 数据库优化
- 合理的索引设计
- 定期备份

## 8. 监控与维护

### 8.1 系统监控
- 服务器监控
- 应用监控
- 数据库监控
- 日志监控

### 8.2 故障处理
- 故障定位
- 故障恢复

### 8.3 系统维护
- 定期更新
- 漏洞修复
- 性能优化
- 数据清理

## 9. 结论

本技术架构设计为采购管理系统提供了一个完整的技术实现方案，包括前端、后端和数据库设计。系统采用前后端分离的架构风格，使用现代的技术栈，具有良好的可扩展性和可维护性。通过合理的系统设计和优化，可以确保系统的性能和安全性，满足计算机零部件制造企业的采购管理需求。