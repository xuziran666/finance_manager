"""系统配置文件：从 .env 文件或环境变量读取所有配置项"""
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 项目根目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ========== 数据库配置（优先从环境变量读取，失败则使用默认值） ==========
DB_HOST = os.getenv('DB_HOST', 'localhost')           # 数据库主机地址
DB_PORT = int(os.getenv('DB_PORT', 3306))              # 数据库端口号
DB_USER = os.getenv('DB_USER', 'root')                 # 数据库用户名
DB_PASS = os.getenv('DB_PASS', '123456')             # 数据库密码
DB_NAME = os.getenv('DB_NAME', 'finance_manager')      # 数据库名称

# ========== Flask 应用配置 ==========
SECRET_KEY = os.getenv('SECRET_KEY', 'finance-manager-secret-key-2024')  # 密钥
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')      # 调试模式
HOST = os.getenv('HOST', '0.0.0.0')   # 监听所有网络接口
PORT = int(os.getenv('PORT', 5000))   # 服务端口号

# ========== 数据库连接池配置 ==========
POOL_MIN = int(os.getenv('POOL_MIN', 2))   # 最小空闲连接数
POOL_MAX = int(os.getenv('POOL_MAX', 10))  # 最大连接数
