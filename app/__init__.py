from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
import os

# 初始化插件
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 未登录跳转页面
login_manager.login_message = '请先登录后再访问该页面'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 绑定插件
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # 注册蓝图
    from app.auth.routes import auth_bp
    from app.competitions.routes import comp_bp
    from app.admin.routes import admin_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(comp_bp, url_prefix='/competitions')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # 注册主页路由（根路径）
    @app.route('/')
    def index():
        return redirect(url_for('competitions.list'))

    return app

# 导入模型（确保模型被识别）
from app.models import user, competition, application