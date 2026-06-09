"""系统配置：基于 pydantic-settings 统一管理配置"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 应用配置
    app_secret_key: str = "finance-manager-secret-key-2026"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 5000

    # JWT 配置
    app_jwt_algorithm: str = "HS256"
    app_jwt_expire_minutes: int = 1440

    # 数据库配置
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "your_password"
    db_name: str = "finance_manager"
    db_pool_min: int = 2
    db_pool_max: int = 10


_settings = _Settings()

SECRET_KEY = _settings.app_secret_key
DEBUG = _settings.app_debug
HOST = _settings.app_host
PORT = _settings.app_port

DB_HOST = _settings.db_host
DB_PORT = _settings.db_port
DB_USER = _settings.db_user
DB_PASSWORD = _settings.db_password
DB_NAME = _settings.db_name
POOL_MIN = _settings.db_pool_min
POOL_MAX = _settings.db_pool_max

JWT_ALGORITHM = _settings.app_jwt_algorithm
JWT_EXPIRE_MINUTES = _settings.app_jwt_expire_minutes
