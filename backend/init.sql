-- ============================================
-- 财务管理系统 - 数据库初始化脚本
-- 数据库名：finance_manager
-- ============================================

CREATE DATABASE IF NOT EXISTS finance_manager CHARACTER SET utf8mb4;
USE finance_manager;

-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. 账户表
CREATE TABLE IF NOT EXISTS accounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    balance DECIMAL(12,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. 交易记录表
CREATE TABLE IF NOT EXISTS transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    account_id INT NOT NULL,
    type VARCHAR(10) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) DEFAULT '',
    amount DECIMAL(12,2) NOT NULL,
    note TEXT,
    date DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. 分类表（用户独立分类）
CREATE TABLE IF NOT EXISTS categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    type VARCHAR(10) NOT NULL,
    main VARCHAR(50) NOT NULL,
    sub VARCHAR(50) DEFAULT '',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 默认分类（系统用户 user_id=-1，注册时自动复制给新用户）
INSERT IGNORE INTO users (id, username, password_hash) VALUES (-1, '_system_', '');
INSERT INTO categories (user_id, type, main, sub) VALUES
(-1, 'income', '工资', '基本工资'),
(-1, 'income', '工资', '奖金'),
(-1, 'income', '工资', '补贴'),
(-1, 'income', '兼职', '线上兼职'),
(-1, 'income', '兼职', '线下兼职'),
(-1, 'income', '投资', '股票收益'),
(-1, 'income', '投资', '基金收益'),
(-1, 'income', '投资', '理财收益'),
(-1, 'income', '红包', '微信红包'),
(-1, 'income', '红包', '礼金'),
(-1, 'income', '其他', '退款'),
(-1, 'income', '其他', '意外收入'),
(-1, 'expense', '餐饮', '早餐'),
(-1, 'expense', '餐饮', '午餐'),
(-1, 'expense', '餐饮', '晚餐'),
(-1, 'expense', '餐饮', '零食饮料'),
(-1, 'expense', '餐饮', '水果'),
(-1, 'expense', '交通', '公交地铁'),
(-1, 'expense', '交通', '打车'),
(-1, 'expense', '交通', '加油'),
(-1, 'expense', '交通', '停车费'),
(-1, 'expense', '购物', '日用品'),
(-1, 'expense', '购物', '服装鞋帽'),
(-1, 'expense', '购物', '数码产品'),
(-1, 'expense', '居住', '房租'),
(-1, 'expense', '居住', '水电燃气'),
(-1, 'expense', '居住', '物业费'),
(-1, 'expense', '居住', '网费'),
(-1, 'expense', '娱乐', '电影'),
(-1, 'expense', '娱乐', '游戏'),
(-1, 'expense', '娱乐', '旅游'),
(-1, 'expense', '娱乐', '运动健身'),
(-1, 'expense', '学习', '书籍'),
(-1, 'expense', '学习', '课程'),
(-1, 'expense', '医疗', '药品'),
(-1, 'expense', '医疗', '体检'),
(-1, 'expense', '医疗', '挂号'),
(-1, 'expense', '通讯', '手机话费'),
(-1, 'expense', '人情', '随礼'),
(-1, 'expense', '人情', '孝敬长辈'),
(-1, 'expense', '其他', '快递费'),
(-1, 'expense', '其他', '维修费'),
(-1, 'expense', '转账', '转账');

-- 5. 预算表
CREATE TABLE IF NOT EXISTS budgets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) DEFAULT '',
    amount DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. 日志表
CREATE TABLE IF NOT EXISTS logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    action VARCHAR(50) NOT NULL,
    detail TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
