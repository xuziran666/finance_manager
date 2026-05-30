# 个人收支管理系统

一个基于 Vue 3 + Flask 的个人财务管理 Web 应用，支持多账户管理、收支记录、分类管理、预算跟踪、统计分析等功能。

## 技术栈

| 前端 | 后端 |
|------|------|
| Vue 3 (Composition API) | Flask 3.0 |
| Vite 8 | PyMySQL + DBUtils 连接池 |
| Element Plus | Python 3 |
| Vue Router 4 | MySQL |
| Axios | |

## 功能

- **财务总览** — 总收入/支出/结余概览，最近交易列表
- **账户管理** — 添加/编辑/删除账户（现金、银行卡、微信、支付宝）
- **收支记录** — 按账户、日期范围筛选，分页展示，添加收支，账户间转账，CSV 导出
- **分类管理** — 收入/支出分类的增删改，支持二级分类
- **预算管理** — 按月设置分类预算，实时预警超支
- **统计分析** — 按账户/日期统计，含分类占比趋势
- **操作日志** — 记录所有关键操作

## 快速开始

### 前置要求

- MySQL 5.7+
- Python 3.10+
- Node.js 18+

### 1. 初始化数据库

```bash
mysql -u root -p < manage_system/init.sql
```

### 2. 配置后端

```bash
cd manage_system
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

编辑 `.env`（可选，默认值可直接使用）：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASS=123456
DB_NAME=finance_manager
```

启动后端：

```bash
python app.py
# 访问 http://localhost:5000
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

Vite 开发服务器已配置代理，`/api/*` 请求自动转发到后端 `http://localhost:5000`。

### 4. 生产构建

```bash
cd frontend
npm run build
# 产物在 dist/ 目录
```

## 项目结构

```
├── frontend/                    # Vue 3 前端
│   ├── src/
│   │   ├── api/                 # API 请求层（按资源拆分）
│   │   │   ├── request.js       #   Axios 实例 + 错误处理
│   │   │   ├── account.js       #   账户相关接口
│   │   │   ├── transaction.js   #   交易相关接口
│   │   │   ├── category.js      #   分类相关接口
│   │   │   ├── budget.js        #   预算相关接口
│   │   │   ├── statistics.js    #   统计相关接口
│   │   │   ├── log.js           #   日志相关接口
│   │   │   └── index.js         #   工具函数（fmt）
│   │   ├── composables/         # 共享状态（useStore）
│   │   ├── layout/              # 布局组件
│   │   ├── router/              # 路由配置（懒加载）
│   │   └── views/               # 页面组件
│   ├── vite.config.js
│   └── package.json
│
├── manage_system/               # Flask 后端
│   ├── app.py                   # 入口
│   ├── config.py                # 配置
│   ├── route/                   # 路由层
│   │   ├── result.py            #   统一响应封装
│   │   ├── account_routes.py
│   │   ├── transaction_routes.py
│   │   ├── category_routes.py
│   │   ├── budget_routes.py
│   │   ├── statistics_routes.py
│   │   └── log_routes.py
│   ├── service/                 # 业务层
│   ├── dao/                     # 数据访问层（纯 SQL）
│   ├── db/                      # 数据库连接池
│   ├── init.sql                 # 数据库初始化脚本
│   └── requirements.txt
│
└── README.md
```

## API 概览

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/accounts` | 获取所有账户 |
| POST | `/api/accounts` | 添加账户 |
| PUT | `/api/accounts/<id>` | 更新账户 |
| DELETE | `/api/accounts/<id>` | 删除账户 |
| GET | `/api/transactions` | 分页查询交易 |
| POST | `/api/transactions` | 添加交易 |
| POST | `/api/transactions/transfer` | 账户间转账 |
| GET | `/api/transactions/export` | 导出 CSV |
| GET | `/api/categories` | 获取分类树 |
| POST | `/api/categories` | 添加分类 |
| PUT | `/api/categories` | 修改分类 |
| DELETE | `/api/categories` | 删除分类 |
| GET | `/api/budgets` | 获取预算 |
| POST | `/api/budgets` | 设置预算 |
| DELETE | `/api/budgets` | 删除预算 |
| GET | `/api/budgets/summary` | 预算汇总 + 预警 |
| GET | `/api/statistics` | 统计分析 |
| GET | `/api/logs` | 操作日志 |

所有接口统一返回 `{ code: 200, data: ..., msg: "成功" }` 格式。

## 数据库

使用 MySQL，连接池由 DBUtils 管理，支持事务上下文自动提交/回滚。

核心表：

- `accounts` — 账户（名称、类型、余额）
- `transactions` — 交易记录（关联账户、类型、分类、金额）
- `categories` — 分类树（收入/支出，支持二级）
- `budgets` — 预算设置（年/月/分类/金额）
- `logs` — 操作日志

## License

MIT
