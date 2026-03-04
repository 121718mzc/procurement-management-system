# 采购管理系统

## 项目概述

采购管理系统是为计算机零部件制造企业设计的一套采购系统，用于采购生产资料和公司运营所需的各类物品器材。系统包含供应商管理、物料管理、价格管理、合同管理和采购订单管理等核心功能。

## 技术栈

### 前端
- Vue 3
- Vite
- Pinia (状态管理)
- Vue Router (路由)
- Element Plus (UI组件库)
- Axios (HTTP客户端)
- jsPDF (PDF导出)

### 后端
- Python 3.9+
- Flask (Web框架)
- SQLAlchemy (ORM)
- MySQL (数据库)
- ReportLab (PDF生成)
- bcrypt (密码加密)

## 项目结构

```
procurement-management-system/
├── procurement-frontend/       # 前端项目
│   ├── public/                 # 静态资源
│   ├── src/                    # 源代码
│   │   ├── views/              # 视图组件
│   │   ├── router/             # 路由配置
│   │   ├── stores/             # 状态管理
│   │   ├── services/           # API服务
│   │   └── utils/              # 工具函数
│   ├── index.html              # 入口HTML
│   ├── package.json            # 前端依赖
│   └── vite.config.js          # Vite配置
├── procurement-backend/        # 后端项目
│   ├── config/                 # 配置文件
│   ├── models/                 # 数据模型
│   ├── routes/                 # 路由和业务逻辑
│   ├── app.py                  # 应用入口
│   ├── db.py                   # 数据库连接
│   ├── run.py                  # 运行脚本
│   ├── simple_app.py           # 简化版应用
│   ├── test_app.py             # 测试应用
│   ├── init_data.py            # 初始化数据
│   ├── generate_materials.py   # 生成物料数据
│   ├── generate_suppliers.py   # 生成供应商数据
│   ├── generate_purchase_orders.py  # 生成采购订单数据
│   └── venv/                   # 虚拟环境
├── database.sql                # 数据库脚本
├── database_relationship.md    # 数据库关系图
├── business_model_relationship.md  # 业务模型关系图
├── business_model_relationship_detailed.md  # 详细业务模型关系图
├── development_plan.md         # 开发计划
└── README.md                   # 项目说明
```

## 环境搭建

### 前端环境
1. 进入前端目录
   ```bash
   cd procurement-frontend
   ```

2. 安装依赖
   ```bash
   npm install
   ```

3. 启动开发服务器
   ```bash
   npm run dev
   ```

### 后端环境
1. 进入后端目录
   ```bash
   cd procurement-backend
   ```

2. 激活虚拟环境
   ```bash
   venv\Scripts\activate  # Windows
   # 或
   source venv/bin/activate  # Linux/Mac
   ```

3. 启动开发服务器
   ```bash
   python run.py
   ```

### 数据库配置
1. 安装MySQL数据库
2. 创建数据库
   ```sql
   CREATE DATABASE procurement_db;
   ```
3. 执行SQL脚本
   ```bash
   mysql -u root -p procurement_db < database.sql
   ```

## 系统功能

### 1. 供应商管理
- 添加、编辑、删除供应商
- 供应商信息查询
- 供应商状态管理

### 2. 物料管理
- 物料分类管理
- 物料信息添加、编辑、删除
- 物料库存管理

### 3. 价格管理
- 供应商物料价格管理
- 价格有效期管理

### 4. 合同管理
- 合同类型管理
- 合同创建、编辑、删除
- 合同PDF导出

### 5. 采购订单管理
- 采购订单创建、编辑、删除
- 采购订单状态管理
- 采购订单物品管理

## 测试账号

- 用户名：buyer
- 密码：123456

## 系统特点

1. **完整性**：覆盖了采购管理的完整业务流程
2. **清晰性**：业务实体之间的关系明确清晰
3. **可扩展性**：支持业务流程的扩展和变更
4. **实用性**：直接对应实际业务操作
5. **安全性**：用户密码加密存储，保护敏感信息

## 注意事项

1. 本系统为演示版本，实际使用时需要根据企业的具体需求进行定制
2. 数据库配置需要根据实际环境进行修改
3. 生产环境部署时需要配置HTTPS和其他安全措施

## 联系方式

如有问题或建议，请联系系统管理员。
