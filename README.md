# 个人收支管理系统

一个基于 Vue 3 + FastAPI 的个人财务管理 Web 应用，支持多账户管理、收支记录、分类管理、预算跟踪、统计分析等功能。

## 技术栈

| 前端 | 后端 |
|------|------|
| Vue 3 (Composition API) | FastAPI |
| Vite | PyMySQL + DBUtils 连接池 |
| Element Plus | Python 3.12+ |
| Vue Router 4 | MySQL |
| Axios | uv 包管理 |

## 功能

- **财务总览** — 总收入/支出/结余概览，最近交易列表
- **账户管理** — 添加/编辑/删除账户（现金、银行卡、微信、支付宝）
- **收支记录** — 按账户、日期范围筛选，分页展示，添加/删除收支，账户间转账，CSV 导出
- **分类管理** — 收入/支出分类的增删改，支持二级分类
- **预算管理** — 按月设置分类预算，实时预警超支
- **统计分析** — 按账户/日期统计，含分类占比趋势
- **操作日志** — 记录所有关键操作，东八区显示

## 快速开始

### 前置要求

- MySQL 5.7+
- Python 3.12+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/)

### 1. 初始化数据库

```bash
mysql -u root -p < backend/init.sql
```

### 2. 配置后端

编辑 `backend/.env`（可选，默认值可直接使用）：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=finance_manager
```

安装依赖并启动：

```bash
cd backend
uv sync
uv run python app.py
# 访问 http://localhost:5000
# API 文档 http://localhost:5000/docs
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
│   │   ├── api/                 # API 请求层
│   │   ├── composables/         # 共享状态
│   │   ├── layout/              # 布局组件
│   │   ├── router/              # 路由配置
│   │   └── views/               # 页面组件
│   ├── vite.config.js
│   └── package.json
│
├── backend/                     # FastAPI 后端
│   ├── app.py                   # 入口
│   ├── config.py                # 配置（环境变量）
│   ├── dto/                     # 请求数据模型
│   │   ├── account.py           #   账户 DTO
│   │   ├── transaction.py       #   交易 DTO
│   │   ├── category.py          #   分类 DTO
│   │   └── budget.py            #   预算 DTO
│   ├── vo/                      # 响应数据模型
│   │   └── result.py            #   统一响应 VO
│   ├── route/                   # 路由层
│   ├── service/                 # 业务层
│   ├── dao/                     # 数据访问层
│   ├── db/                      # 数据库连接池
│   ├── tests/                   # 测试
│   ├── init.sql                 # 数据库初始化脚本
│   └── pyproject.toml
│
└── README.md
```

## API 概览

| 方法 | 路径 | 用途 |
|------|------|------|
| GET | `/api/accounts` | 获取所有账户 |
| POST | `/api/accounts` | 添加账户 |
| PUT | `/api/accounts/{id}` | 更新账户 |
| DELETE | `/api/accounts/{id}` | 删除账户 |
| GET | `/api/transactions` | 分页查询交易 |
| POST | `/api/transactions` | 添加交易 |
| DELETE | `/api/transactions/{id}` | 删除交易 |
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

所有接口统一返回 `{ code: 200, data: ..., msg: "成功" }` 格式。自动生成 OpenAPI 文档，访问 `http://localhost:5000/docs` 在线调试。

## 数据库

使用 MySQL，连接池由 DBUtils 管理，支持事务上下文自动提交/回滚。MySQL session 时区默认设为 `+08:00`。

核心表：

- `accounts` — 账户（名称、类型、余额）
- `transactions` — 交易记录（关联账户、类型、分类、金额）
- `categories` — 分类树（收入/支出，支持二级）
- `budgets` — 预算设置（年/月/分类/金额）
- `logs` — 操作日志

## License

MIT
