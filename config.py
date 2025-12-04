import os
from datetime import timedelta

class Config:
    # 密钥（用于CSRF保护、Session加密）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'phg-2025-secret-key-keep-safe'
    # 数据库配置（SQLite，无需额外安装数据库，文件存储）
    SQLALCHEMY_DATABASE_URI = 'sqlite:///phg.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭不必要的警告
    # 上传文件配置（参赛申请可上传材料）
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 最大上传16MB
    # GDPR配置
    DATA_RETENTION_PERIOD = timedelta(days=365)  # 数据保留1年
    PRIVACY_POLICY_URL = '/static/docs/privacy.pdf'  # 隐私政策路径

# 创建上传文件夹（若不存在）
if not os.path.exists(Config.UPLOAD_FOLDER):
    os.makedirs(Config.UPLOAD_FOLDER)
