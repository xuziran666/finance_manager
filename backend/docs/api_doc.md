# 财务管理系统 - API 接口文档

> 基础URL：`http://localhost:5000`（默认）
> 
> 所有 API 以 `/api` 为前缀，响应格式统一为 JSON。

---

## 一、通用响应格式

### ✅ 成功响应

```json
{
    "code": 200,
    "data": { ... },
    "msg": "成功"
}
```

### ❌ 失败响应

```json
{
    "code": 400,
    "msg": "错误描述信息"
}
```

| 字段     | 类型           | 说明                   |
| ------ | ------------ | -------------------- |
| `code` | int          | 状态码（200=成功，400=业务错误） |
| `data` | object/array | 响应数据（成功时返回）          |
| `msg`  | string       | 提示信息                 |

---

## 二、账户管理（Accounts）

### 2.1 获取所有账户列表

> **GET** `/api/accounts`

**请求参数：** 无

**响应示例：**

```json
{
    "code": 200,
    "data": [
        {
            "id": 1,
            "name": "工资卡",
            "type": "bank",
            "balance": 15000.00,
            "created_at": "2026-01-01 10:00:00"
        },
        {
            "id": 2,
            "name": "支付宝",
            "type": "alipay",
            "balance": 3000.50,
            "created_at": "2026-01-01 10:00:00"
        }
    ],
    "msg": "成功"
}
```

---

### 2.2 添加账户

> **POST** `/api/accounts`

**请求体（JSON）：**

| 字段        | 类型     | 必填  | 说明                                 |
| --------- | ------ | --- | ---------------------------------- |
| `name`    | string | 是   | 账户名称                               |
| `type`    | string | 是   | 账户类型（如：cash, bank, alipay, wechat） |
| `balance` | number | 否   | 初始余额，默认 0，不能为负                     |

**请求示例：**

```json
{
    "name": "储蓄卡",
    "type": "bank",
    "balance": 5000.00
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": {
        "id": 3,
        "name": "储蓄卡",
        "type": "bank",
        "balance": 5000.00,
        "created_at": "2026-01-15 14:30:00"
    },
    "msg": "成功"
}
```

---

### 2.3 更新账户

> **PUT** `/api/accounts/{id}`

**路径参数：**

| 参数   | 类型  | 说明   |
| ---- | --- | ---- |
| `id` | int | 账户ID |

**请求体（JSON）：**

| 字段     | 类型     | 必填  | 说明  |
| ------ | ------ | --- | --- |
| `name` | string | 否   | 新名称 |
| `type` | string | 否   | 新类型 |

**请求示例：**

```json
{
    "name": "工资储蓄卡",
    "type": "bank"
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": {
        "id": 1,
        "name": "工资储蓄卡",
        "type": "bank",
        "balance": 15000.00,
        "created_at": "2026-01-01 10:00:00"
    },
    "msg": "成功"
}
```

---

### 2.4 删除账户

> **DELETE** `/api/accounts/{id}`

**路径参数：**

| 参数   | 类型  | 说明   |
| ---- | --- | ---- |
| `id` | int | 账户ID |

**响应示例：**

```json
{
    "code": 200,
    "data": null,
    "msg": "删除成功"
}
```

> ⚠️ 删除账户会同时删除该账户下的所有交易记录（级联删除）。

---

## 三、交易记录管理（Transactions）

### 3.1 获取交易记录列表（分页）

> **GET** `/api/transactions`

**查询参数（Query String）：**

| 参数           | 类型     | 必填  | 默认值 | 说明                       |
| ------------ | ------ | --- | --- | ------------------------ |
| `account_id` | int    | 否   |     | 按账户筛选                    |
| `start_date` | string | 否   |     | 起始日期（>=），格式：`YYYY-MM-DD` |
| `end_date`   | string | 否   |     | 结束日期（<=），格式：`YYYY-MM-DD` |
| `category`   | string | 否   |     | 按分类筛选                    |
| `page`       | int    | 否   | 1   | 页码                       |
| `page_size`  | int    | 否   | 20  | 每页条数                     |

**响应示例：**

```json
{
    "code": 200,
    "data": {
        "transactions": [
            {
                "id": 1,
                "account_id": 1,
                "type": "expense",
                "category": "餐饮",
                "subcategory": "午餐",
                "amount": 25.00,
                "note": "食堂吃饭",
                "date": "2026-01-15",
                "created_at": "2026-01-15 12:00:00",
                "account_name": "工资卡",
                "account_type": "bank"
            }
        ],
        "total": 1,
        "page": 1,
        "page_size": 20,
        "total_pages": 1
    },
    "msg": "成功"
}
```

| 响应字段           | 类型    | 说明        |
| -------------- | ----- | --------- |
| `transactions` | array | 交易记录列表    |
| `total`        | int   | 符合条件的总记录数 |
| `page`         | int   | 当前页码      |
| `page_size`    | int   | 每页条数      |
| `total_pages`  | int   | 总页数       |

---

### 3.2 添加交易记录

> **POST** `/api/transactions`

**请求体（JSON）：**

| 字段            | 类型     | 必填  | 默认值 | 说明                             |
| ------------- | ------ | --- | --- | ------------------------------ |
| `account_id`  | int    | 是   |     | 账户ID                           |
| `type`        | string | 是   |     | 类型：`income`（收入）/ `expense`（支出） |
| `category`    | string | 是   |     | 分类名称                           |
| `amount`      | number | 是   |     | 金额，不能为负                        |
| `note`        | string | 否   | ""  | 备注                             |
| `date`        | string | 否   | 当天  | 日期，格式：`YYYY-MM-DD`             |
| `subcategory` | string | 否   | ""  | 二级分类名称                         |

**请求示例：**

```json
{
    "account_id": 1,
    "type": "expense",
    "category": "餐饮",
    "subcategory": "午餐",
    "amount": 25.00,
    "note": "食堂",
    "date": "2026-05-20"
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": {
        "id": 100,
        "account_id": 1,
        "type": "expense",
        "category": "餐饮",
        "subcategory": "午餐",
        "amount": 25.00,
        "note": "食堂",
        "date": "2026-05-20",
        "account_name": "工资卡",
        "account_type": "bank"
    },
    "msg": "成功"
}
```

> 💡 添加交易记录后，系统会自动更新对应账户的余额（收入增加，支出减少）。

---

### 3.3 转账

> **POST** `/api/transactions/transfer`

在两个账户之间进行资金转账，会同时生成一笔支出（转出方）和一笔收入（转入方）记录。

**请求体（JSON）：**

| 字段             | 类型     | 必填  | 默认值 | 说明          |
| -------------- | ------ | --- | --- | ----------- |
| `from_account` | int    | 是   |     | 转出账户ID      |
| `to_account`   | int    | 是   |     | 转入账户ID      |
| `amount`       | number | 是   |     | 转账金额，必须 > 0 |
| `note`         | string | 否   | ""  | 转账备注        |

**请求示例：**

```json
{
    "from_account": 1,
    "to_account": 2,
    "amount": 500.00,
    "note": "还钱"
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": null,
    "msg": "转账成功"
}
```

**校验规则：**

- 转出和转入账户不能相同
- 转出账户余额必须 ≥ 转账金额
- 金额必须 > 0

---

### 3.4 导出交易记录（CSV）

> **GET** `/api/transactions/export`

**查询参数（Query String）：**

| 参数           | 类型     | 必填  | 说明    |
| ------------ | ------ | --- | ----- |
| `account_id` | int    | 否   | 按账户筛选 |
| `start_date` | string | 否   | 起始日期  |
| `end_date`   | string | 否   | 结束日期  |

**响应：** 返回 CSV 文件（`Content-Type: text/csv;charset=utf-8`）

**CSV 列头：**

```
日期,类型,分类,二级分类,金额,账户,备注
```

**导出示例：**

```
日期,类型,分类,二级分类,金额,账户,备注
2026-05-20,支出,餐饮,午餐,25.00,工资卡,食堂
2026-05-19,收入,工资,基本工资,8000.00,工资卡,5月工资
```

---

## 四、分类管理（Categories）

### 4.1 获取所有分类

> **GET** `/api/categories`

**请求参数：** 无

**响应示例：**

```json
{
    "code": 200,
    "data": {
        "tree": {
            "income": {
                "工资": ["基本工资", "奖金", "补贴"],
                "兼职": ["线上兼职", "线下兼职"],
                "投资": ["股票收益", "基金收益", "理财收益"],
                "红包": ["微信红包", "礼金"],
                "其他": ["退款", "意外收入"]
            },
            "expense": {
                "餐饮": ["早餐", "午餐", "晚餐", "零食饮料", "水果"],
                "交通": ["公交地铁", "打车", "加油", "停车费"],
                "购物": ["日用品", "服装鞋帽", "数码产品"],
                "居住": ["房租", "水电燃气", "物业费", "网费"],
                "娱乐": ["电影", "游戏", "旅游", "运动健身"],
                "学习": ["书籍", "课程"],
                "医疗": ["药品", "体检", "挂号"],
                "通讯": ["手机话费"],
                "人情": ["随礼", "孝敬长辈"],
                "其他": ["快递费", "维修费"],
                "转账": ["转账"]
            }
        },
        "flat": [
            {
                "id": 1,
                "type": "income",
                "main": "工资",
                "sub": "基本工资"
            }
        ]
    },
    "msg": "成功"
}
```

| 响应字段   | 类型     | 说明                              |
| ------ | ------ | ------------------------------- |
| `tree` | object | 树形结构：type → main → [sub, ...]   |
| `flat` | array  | 扁平列表，每条记录包含 id, type, main, sub |

---

### 4.2 添加分类

> **POST** `/api/categories`

**请求体（JSON）：**

| 字段     | 类型     | 必填  | 默认值 | 说明                      |
| ------ | ------ | --- | --- | ----------------------- |
| `type` | string | 是   |     | 类型：`income` / `expense` |
| `main` | string | 是   |     | 主分类名称                   |
| `sub`  | string | 否   | ""  | 二级分类名称                  |

**请求示例：**

```json
{
    "type": "expense",
    "main": "宠物",
    "sub": "猫粮"
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": null,
    "msg": "添加成功"
}
```

**校验规则：** 同一 type + main + sub 组合不能重复

---

### 4.3 修改分类

> **PUT** `/api/categories`

**请求体（JSON）：**

| 字段         | 类型     | 必填  | 说明    |
| ---------- | ------ | --- | ----- |
| `old_type` | string | 是   | 原类型   |
| `old_main` | string | 是   | 原主分类  |
| `old_sub`  | string | 是   | 原二级分类 |
| `new_type` | string | 是   | 新类型   |
| `new_main` | string | 是   | 新主分类  |
| `new_sub`  | string | 是   | 新二级分类 |

**请求示例：**

```json
{
    "old_type": "expense",
    "old_main": "餐饮",
    "old_sub": "午餐",
    "new_type": "expense",
    "new_main": "餐饮",
    "new_sub": "工作午餐"
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": null,
    "msg": "修改成功"
}
```

---

### 4.4 删除分类

> **DELETE** `/api/categories`

**请求体（JSON）：**

| 字段     | 类型     | 必填  | 默认值 | 说明   |
| ------ | ------ | --- | --- | ---- |
| `type` | string | 是   |     | 类型   |
| `main` | string | 是   |     | 主分类  |
| `sub`  | string | 否   | ""  | 二级分类 |

**请求示例：**

```json
{
    "type": "expense",
    "main": "宠物",
    "sub": "猫粮"
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": null,
    "msg": "删除成功"
}
```

---

## 五、预算管理（Budgets）

### 5.1 获取预算列表

> **GET** `/api/budgets`

**查询参数（Query String）：**

| 参数      | 类型  | 必填  | 说明                |
| ------- | --- | --- | ----------------- |
| `year`  | int | 否   | 年份，不传则查所有年份       |
| `month` | int | 否   | 月份（1-12），不传则查所有月份 |

**响应示例：**

```json
{
    "code": 200,
    "data": [
        {
            "id": 1,
            "year": 2026,
            "month": 5,
            "category": "餐饮",
            "subcategory": "",
            "amount": 2000.00
        },
        {
            "id": 2,
            "year": 2026,
            "month": 5,
            "category": "交通",
            "subcategory": "",
            "amount": 500.00
        }
    ],
    "msg": "成功"
}
```

---

### 5.2 设置预算

> **POST** `/api/budgets`

> ⚠️ 如果该年月分类的预算已存在，则覆盖更新金额；否则新增一条记录。

**请求体（JSON）：**

| 字段         | 类型     | 必填  | 说明        |
| ---------- | ------ | --- | --------- |
| `year`     | int    | 是   | 年份        |
| `month`    | int    | 是   | 月份（1-12）  |
| `category` | string | 是   | 分类名称      |
| `amount`   | number | 是   | 预算金额，不能为负 |

**请求示例：**

```json
{
    "year": 2026,
    "month": 6,
    "category": "餐饮",
    "amount": 2500.00
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": null,
    "msg": "设置成功"
}
```

---

### 5.3 获取预算汇总（含花费统计和预警）

> **GET** `/api/budgets/summary`

**查询参数（Query String）：**

| 参数      | 类型  | 必填  | 默认值 | 说明  |
| ------- | --- | --- | --- | --- |
| `year`  | int | 否   | 当前年 | 年份  |
| `month` | int | 否   | 当前月 | 月份  |

**响应示例：**

```json
{
    "code": 200,
    "data": {
        "summary": [
            {
                "category": "餐饮",
                "budget": 2000.00,
                "spent": 1250.50,
                "remaining": 749.50,
                "percentage": 62.5,
                "status": "normal"
            },
            {
                "category": "交通",
                "budget": 500.00,
                "spent": 480.00,
                "remaining": 20.00,
                "percentage": 96.0,
                "status": "normal"
            },
            {
                "category": "总计",
                "budget": 2500.00,
                "spent": 1730.50,
                "remaining": 769.50,
                "percentage": 69.2,
                "status": "normal"
            }
        ],
        "warnings": [
            "餐饮已用62.5%",
            "交通已用96.0%"
        ]
    },
    "msg": "成功"
}
```

| 汇总字段         | 类型     | 说明                               |
| ------------ | ------ | -------------------------------- |
| `category`   | string | 分类名称，最后一条为"总计"                   |
| `budget`     | number | 预算金额                             |
| `spent`      | number | 实际花费                             |
| `remaining`  | number | 剩余预算                             |
| `percentage` | number | 花费百分比（0-100）                     |
| `status`     | string | 状态：`normal`（正常）/ `overspent`（超支） |
| `warnings`   | array  | 预警列表（超支或使用达 80%+ 时提示）            |

---

### 5.4 删除预算

> **DELETE** `/api/budgets`

**请求体（JSON）：**

| 字段         | 类型     | 必填  | 默认值 | 说明              |
| ---------- | ------ | --- | --- | --------------- |
| `year`     | int    | 是   |     | 年份              |
| `month`    | int    | 是   |     | 月份              |
| `category` | string | 否   | ""  | 分类名称（不传则删除该月全部） |

**请求示例：**

```json
{
    "year": 2026,
    "month": 6,
    "category": "餐饮"
}
```

**响应示例：**

```json
{
    "code": 200,
    "data": null,
    "msg": "删除成功"
}
```

---

## 六、统计报表（Statistics）

### 6.1 获取统计数据

> **GET** `/api/statistics`

**查询参数（Query String）：**

| 参数           | 类型     | 必填  | 默认值     | 说明                                                |
| ------------ | ------ | --- | ------- | ------------------------------------------------- |
| `account_id` | int    | 否   |         | 按账户筛选                                             |
| `start_date` | string | 否   |         | 起始日期，格式：`YYYY-MM-DD`                              |
| `end_date`   | string | 否   |         | 结束日期，格式：`YYYY-MM-DD`                              |
| `group_by`   | string | 否   | `month` | 时间分组方式：`year`（年）/ `month`（月）/ `day`（日）/ `week`（周） |

**响应示例：**

```json
{
    "code": 200,
    "data": {
        "total_income": 15000.00,
        "total_expense": 8650.50,
        "balance": 6349.50,
        "trend": [
            {
                "period": "2026-01",
                "income": 8000.00,
                "expense": 3200.00,
                "balance": 4800.00
            },
            {
                "period": "2026-02",
                "income": 7000.00,
                "expense": 5450.50,
                "balance": 1549.50
            }
        ],
        "expense_by_category": [
            {"name": "餐饮", "amount": 3200.00},
            {"name": "居住", "amount": 2500.00},
            {"name": "交通", "amount": 850.50}
        ],
        "income_by_category": [
            {"name": "工资", "amount": 13000.00},
            {"name": "兼职", "amount": 2000.00}
        ]
    },
    "msg": "成功"
}
```

| 响应字段                  | 类型     | 说明              |
| --------------------- | ------ | --------------- |
| `total_income`        | number | 总收入             |
| `total_expense`       | number | 总支出             |
| `balance`             | number | 结余（收入-支出）       |
| `trend`               | array  | 按时间分组趋势         |
| `trend[].period`      | string | 时间周期（如：2026-01） |
| `trend[].income`      | number | 该周期收入           |
| `trend[].expense`     | number | 该周期支出           |
| `trend[].balance`     | number | 该周期结余           |
| `expense_by_category` | array  | 支出按分类汇总（降序）     |
| `income_by_category`  | array  | 收入按分类汇总（降序）     |

---

## 七、操作日志（Logs）

### 7.1 获取操作日志

> **GET** `/api/logs`

**查询参数（Query String）：**

| 参数      | 类型  | 必填  | 默认值 | 说明       |
| ------- | --- | --- | --- | -------- |
| `limit` | int | 否   | 100 | 返回记录条数上限 |

**响应示例：**

```json
{
    "code": 200,
    "data": [
        {
            "id": 10,
            "time": "2026-05-20 14:30:00",
            "user": "system",
            "action": "ADD_TRANSACTION",
            "detail": "账户[1] expense:25.00"
        },
        {
            "id": 9,
            "time": "2026-05-20 12:00:00",
            "user": "system",
            "action": "ADD_ACCOUNT",
            "detail": "添加账户:储蓄卡"
        }
    ],
    "msg": "成功"
}
```

**action 枚举值说明：**

| action 值          | 说明      |
| ----------------- | ------- |
| `ADD_ACCOUNT`     | 添加账户    |
| `UPDATE_ACCOUNT`  | 更新账户    |
| `DELETE_ACCOUNT`  | 删除账户    |
| `ADD_TRANSACTION` | 添加交易记录  |
| `TRANSFER`        | 转账      |
| `SET_BUDGET`      | 设置/更新预算 |
| `ADD_CATEGORY`    | 添加分类    |
| `UPDATE_CATEGORY` | 更新分类    |
| `DELETE_CATEGORY` | 删除分类    |

---

## 八、接口总览表

| 序号  | 方法     | 路径                           | 说明            |
| --- | ------ | ---------------------------- | ------------- |
| 1   | GET    | `/api/accounts`              | 获取所有账户列表      |
| 2   | POST   | `/api/accounts`              | 添加账户          |
| 3   | PUT    | `/api/accounts/{id}`         | 更新账户          |
| 4   | DELETE | `/api/accounts/{id}`         | 删除账户          |
| 5   | GET    | `/api/transactions`          | 获取交易记录列表（分页）  |
| 6   | POST   | `/api/transactions`          | 添加交易记录        |
| 7   | POST   | `/api/transactions/transfer` | 转账            |
| 8   | GET    | `/api/transactions/export`   | 导出交易记录为CSV    |
| 9   | GET    | `/api/categories`            | 获取所有分类（树形+扁平） |
| 10  | POST   | `/api/categories`            | 添加分类          |
| 11  | PUT    | `/api/categories`            | 修改分类          |
| 12  | DELETE | `/api/categories`            | 删除分类          |
| 13  | GET    | `/api/budgets`               | 获取预算列表        |
| 14  | POST   | `/api/budgets`               | 设置预算          |
| 15  | GET    | `/api/budgets/summary`       | 预算汇总（含预警）     |
| 16  | DELETE | `/api/budgets`               | 删除预算          |
| 17  | GET    | `/api/statistics`            | 统计数据          |
| 18  | GET    | `/api/logs`                  | 操作日志          |