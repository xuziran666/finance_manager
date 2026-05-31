# 财务管理系统 - 数据库文档

> 数据库名称：`finance_manager`
> 字符集：`utf8mb4`
> 引擎：`InnoDB`

---

## 一、数据库概览

本系统共包含 **5张数据表**，分别用于管理账户、交易记录、分类、预算和操作日志。

| 表名             | 中文名   | 功能说明                |
| -------------- | ----- | ------------------- |
| `accounts`     | 账户表   | 存储用户账户（现金、银行卡、支付宝等） |
| `transactions` | 交易记录表 | 存储收入和支出流水明细         |
| `categories`   | 分类表   | 预定义和自定义的收入/支出分类     |
| `budgets`      | 预算表   | 每月各分类预算金额           |
| `logs`         | 日志表   | 系统操作日志              |

### 实体关系图（ER图）

```
accounts (1) ──── (N) transactions
categories ──── (参照) ──── transactions (通过 category 字段)
categories ──── (参照) ──── budgets (通过 category 字段)
```

---

## 二、表结构详细说明

### 2.1 账户表（`accounts`）

存储用户的所有资金账户信息。

| 字段名          | 类型            | 约束                          | 默认值               | 说明                                 |
| ------------ | ------------- | --------------------------- | ----------------- | ---------------------------------- |
| `id`         | INT           | PRIMARY KEY, AUTO_INCREMENT |                   | 主键ID                               |
| `name`       | VARCHAR(50)   | NOT NULL                    |                   | 账户名称（如：工资卡、支付宝）                    |
| `type`       | VARCHAR(20)   | NOT NULL                    |                   | 账户类型（如：cash, bank, alipay, wechat） |
| `balance`    | DECIMAL(12,2) |                             | 0.00              | 当前余额                               |
| `created_at` | TIMESTAMP     |                             | CURRENT_TIMESTAMP | 创建时间                               |

**建表语句：**

```sql
CREATE TABLE IF NOT EXISTS accounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    balance DECIMAL(12,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 2.2 交易记录表（`transactions`）

存储每一笔收入或支出的明细记录。

| 字段名           | 类型            | 约束                          | 默认值               | 说明                             |
| ------------- | ------------- | --------------------------- | ----------------- | ------------------------------ |
| `id`          | INT           | PRIMARY KEY, AUTO_INCREMENT |                   | 主键ID                           |
| `account_id`  | INT           | NOT NULL, FK → accounts(id) |                   | 所属账户ID，级联删除                    |
| `type`        | VARCHAR(10)   | NOT NULL                    |                   | 类型：`income`（收入）/ `expense`（支出） |
| `category`    | VARCHAR(50)   | NOT NULL                    |                   | 主分类名称（如：餐饮、交通、工资）              |
| `subcategory` | VARCHAR(50)   |                             | ''                | 二级分类名称（如：午餐、公交地铁）              |
| `amount`      | DECIMAL(12,2) | NOT NULL                    |                   | 金额                             |
| `note`        | TEXT          |                             |                   | 备注说明                           |
| `date`        | DATE          | NOT NULL                    |                   | 交易日期                           |
| `created_at`  | TIMESTAMP     |                             | CURRENT_TIMESTAMP | 创建时间                           |

**建表语句：**

```sql
CREATE TABLE IF NOT EXISTS transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    type VARCHAR(10) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) DEFAULT '',
    amount DECIMAL(12,2) NOT NULL,
    note TEXT,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**索引说明：**

- 外键 `account_id` → `accounts(id)`，级联删除
- `date` 字段常用于按日期范围筛选

---

### 2.3 分类表（`categories`）

存储收入/支出的分类层级结构，支持二级分类。

| 字段名    | 类型          | 约束                          | 默认值 | 说明                             |
| ------ | ----------- | --------------------------- | --- | ------------------------------ |
| `id`   | INT         | PRIMARY KEY, AUTO_INCREMENT |     | 主键ID                           |
| `type` | VARCHAR(10) | NOT NULL                    |     | 类型：`income`（收入）/ `expense`（支出） |
| `main` | VARCHAR(50) | NOT NULL                    |     | 主分类名称                          |
| `sub`  | VARCHAR(50) |                             | ''  | 二级分类名称                         |

**建表语句：**

```sql
CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(10) NOT NULL,
    main VARCHAR(50) NOT NULL,
    sub VARCHAR(50) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**默认分类数据（通过 `init.sql` 初始化）：**

| type    | main | sub  |
| ------- | ---- | ---- |
| income  | 工资   | 基本工资 |
| income  | 工资   | 奖金   |
| income  | 工资   | 补贴   |
| income  | 兼职   | 线上兼职 |
| income  | 兼职   | 线下兼职 |
| income  | 投资   | 股票收益 |
| income  | 投资   | 基金收益 |
| income  | 投资   | 理财收益 |
| income  | 红包   | 微信红包 |
| income  | 红包   | 礼金   |
| income  | 其他   | 退款   |
| income  | 其他   | 意外收入 |
| expense | 餐饮   | 早餐   |
| expense | 餐饮   | 午餐   |
| expense | 餐饮   | 晚餐   |
| expense | 餐饮   | 零食饮料 |
| expense | 餐饮   | 水果   |
| expense | 交通   | 公交地铁 |
| expense | 交通   | 打车   |
| expense | 交通   | 加油   |
| expense | 交通   | 停车费  |
| expense | 购物   | 日用品  |
| expense | 购物   | 服装鞋帽 |
| expense | 购物   | 数码产品 |
| expense | 居住   | 房租   |
| expense | 居住   | 水电燃气 |
| expense | 居住   | 物业费  |
| expense | 居住   | 网费   |
| expense | 娱乐   | 电影   |
| expense | 娱乐   | 游戏   |
| expense | 娱乐   | 旅游   |
| expense | 娱乐   | 运动健身 |
| expense | 学习   | 书籍   |
| expense | 学习   | 课程   |
| expense | 医疗   | 药品   |
| expense | 医疗   | 体检   |
| expense | 医疗   | 挂号   |
| expense | 通讯   | 手机话费 |
| expense | 人情   | 随礼   |
| expense | 人情   | 孝敬长辈 |
| expense | 其他   | 快递费  |
| expense | 其他   | 维修费  |
| expense | 转账   | 转账   |

---

### 2.4 预算表（`budgets`）

存储每个月各分类的预算金额。

| 字段名           | 类型            | 约束                          | 默认值 | 说明         |
| ------------- | ------------- | --------------------------- | --- | ---------- |
| `id`          | INT           | PRIMARY KEY, AUTO_INCREMENT |     | 主键ID       |
| `year`        | INT           | NOT NULL                    |     | 年份（如：2026） |
| `month`       | INT           | NOT NULL                    |     | 月份（1-12）   |
| `category`    | VARCHAR(50)   | NOT NULL                    |     | 预算分类名称     |
| `subcategory` | VARCHAR(50)   |                             | ''  | 二级分类名称     |
| `amount`      | DECIMAL(12,2) | NOT NULL                    |     | 预算金额       |

**建表语句：**

```sql
CREATE TABLE IF NOT EXISTS budgets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    month INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) DEFAULT '',
    amount DECIMAL(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

### 2.5 日志表（`logs`）

记录系统操作日志，用于审计和追溯。

| 字段名      | 类型          | 约束                          | 默认值               | 说明               |
| -------- | ----------- | --------------------------- | ----------------- | ---------------- |
| `id`     | INT         | PRIMARY KEY, AUTO_INCREMENT |                   | 主键ID             |
| `time`   | TIMESTAMP   |                             | CURRENT_TIMESTAMP | 操作时间             |
| `user`   | VARCHAR(50) |                             | 'system'          | 操作人（当前固定为system） |
| `action` | VARCHAR(50) | NOT NULL                    |                   | 操作类型标识           |
| `detail` | TEXT        |                             |                   | 操作详情描述           |

**建表语句：**

```sql
CREATE TABLE IF NOT EXISTS logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user VARCHAR(50) DEFAULT 'system',
    action VARCHAR(50) NOT NULL,
    detail TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**action 操作类型枚举：**

| action 值          | 说明     |
| ----------------- | ------ |
| `ADD_ACCOUNT`     | 添加账户   |
| `UPDATE_ACCOUNT`  | 更新账户   |
| `DELETE_ACCOUNT`  | 删除账户   |
| `ADD_TRANSACTION` | 添加交易记录 |
| `TRANSFER`        | 转账操作   |
| `SET_BUDGET`      | 设置预算   |
| `ADD_CATEGORY`    | 添加分类   |
| `UPDATE_CATEGORY` | 更新分类   |
| `DELETE_CATEGORY` | 删除分类   |

---

## 三、数据库配置

| 配置项   | 默认值               | 说明                    |
| ----- | ----------------- | --------------------- |
| 主机    | `localhost`       | 可通过环境变量 `DB_HOST` 配置  |
| 端口    | `3306`            | 可通过环境变量 `DB_PORT` 配置  |
| 用户名   | `root`            | 可通过环境变量 `DB_USER` 配置  |
| 密码    | `123456`          | 可通过环境变量 `DB_PASS` 配置  |
| 数据库名  | `finance_manager` | 可通过环境变量 `DB_NAME` 配置  |
| 最小连接池 | `2`               | 可通过环境变量 `POOL_MIN` 配置 |
| 最大连接池 | `10`              | 可通过环境变量 `POOL_MAX` 配置 |

连接池使用 `dbutils.pooled_db.PooledDB`，数据库驱动为 `pymysql`，游标类型为 `DictCursor`（返回字典格式结果）。

---

## 四、数据库操作说明

### 初始化数据库

```bash
mysql -u root -p < init.sql
```