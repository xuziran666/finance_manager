"""项目启动入口：创建 Flask 应用实例并启动开发服务器"""
import os
import sys

# 将项目根目录加入 Python 模块搜索路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS
from config import SECRET_KEY, DEBUG, HOST, PORT
from route import api

# 创建 Flask 应用实例
app = Flask(__name__)
# 配置密钥用于 session 等安全功能
app.config["SECRET_KEY"] = SECRET_KEY
# 启用跨域支持，允许前端开发服务器跨域访问
CORS(app)
# 注册 API 蓝图，所有接口以 /api 为前缀
app.register_blueprint(api)

if __name__ == "__main__":
    # 启动开发服务器
    print(f"服务启动于 http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)