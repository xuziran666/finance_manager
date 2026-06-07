-- ============================================
-- 财务管理系统 - 数据库初始化脚本
-- 数据库名：finance_manager
-- ============================================
-- 如已有数据库，请执行迁移：
-- ALTER TABLE transactions MODIFY date DATETIME NOT NULL;

-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS finance_manager CHARACTER SET utf8mb4;

-- 2. 使用数据库
USE finance_manager;

-- ============================================
-- 3. 创建表结构
-- ============================================

-- 3.1 账户表
CREATE TABLE IF NOT EXISTS accounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    balance DECIMAL(12,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3.2 交易记录表
CREATE TABLE IF NOT EXISTS transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    type VARCHAR(10) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) DEFAULT '',
    amount DECIMAL(12,2) NOT NULL,
    note TEXT,
    date DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3.3 分类表
CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(10) NOT NULL,
    main VARCHAR(50) NOT NULL,
    sub VARCHAR(50) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3.4 预算表
CREATE TABLE IF NOT EXISTS budgets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    month INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) DEFAULT '',
    amount DECIMAL(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3.5 日志表
CREATE TABLE IF NOT EXISTS logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user VARCHAR(50) DEFAULT 'system',
    action VARCHAR(50) NOT NULL,
    detail TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- 4. 初始化默认分类数据
-- ============================================
INSERT INTO categories (type, main, sub) VALUES
-- 收入分类
('income', '工资', '基本工资'),
('income', '工资', '奖金'),
('income', '工资', '补贴'),
('income', '兼职', '线上兼职'),
('income', '兼职', '线下兼职'),
('income', '投资', '股票收益'),
('income', '投资', '基金收益'),
('income', '投资', '理财收益'),
('income', '红包', '微信红包'),
('income', '红包', '礼金'),
('income', '其他', '退款'),
('income', '其他', '意外收入'),
-- 支出分类
('expense', '餐饮', '早餐'),
('expense', '餐饮', '午餐'),
('expense', '餐饮', '晚餐'),
('expense', '餐饮', '零食饮料'),
('expense', '餐饮', '水果'),
('expense', '交通', '公交地铁'),
('expense', '交通', '打车'),
('expense', '交通', '加油'),
('expense', '交通', '停车费'),
('expense', '购物', '日用品'),
('expense', '购物', '服装鞋帽'),
('expense', '购物', '数码产品'),
('expense', '居住', '房租'),
('expense', '居住', '水电燃气'),
('expense', '居住', '物业费'),
('expense', '居住', '网费'),
('expense', '娱乐', '电影'),
('expense', '娱乐', '游戏'),
('expense', '娱乐', '旅游'),
('expense', '娱乐', '运动健身'),
('expense', '学习', '书籍'),
('expense', '学习', '课程'),
('expense', '医疗', '药品'),
('expense', '医疗', '体检'),
('expense', '医疗', '挂号'),
('expense', '通讯', '手机话费'),
('expense', '人情', '随礼'),
('expense', '人情', '孝敬长辈'),
('expense', '其他', '快递费'),
('expense', '其他', '维修费'),
('expense', '转账', '转账');
