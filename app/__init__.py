from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config
import os
from datetime import datetime, timedelta

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

    with app.app_context():
        os.makedirs(app.instance_path, exist_ok=True)

        db.create_all()

        from app.models.user import User
        from app.models.competition import Competition

        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@phg.com',
                password='Admin123!',  # 复用 User 模型的 password setter 自动加密
                consent_given=True,
                is_admin=True
            )
            db.session.add(admin)

        if not Competition.query.first():
            sample_competitions = [
                Competition(
                    name="2025 Highland Dance Competition",
                    category="Individual",
                    start_date=datetime.utcnow() + timedelta(days=30),
                    application_deadline=datetime.utcnow() + timedelta(days=15),
                    description="Traditional Scottish Highland dance competition, divided into solo jazz dance and duet tap dance categories. Contestants must submit a dance video as application material. Judges will score based on movement standardization and sense of rhythm."
                ),
                Competition(
                    name="Bagpipe Ensemble Competition",
                    category="Team",
                    start_date=datetime.utcnow() + timedelta(days=45),
                    application_deadline=datetime.utcnow() + timedelta(days=20),
                    description="Team bagpipe performance competition. Each team consists of 3-5 members. Contestants must perform the designated traditional Scottish tune 'Scotland the Brave' with a performance duration of 5 minutes. Scoring criteria include tone, coordination, and expressiveness."
                ),
                Competition(
                    name="Highland Weightlifting Challenge",
                    category="Mixed",
                    start_date=datetime.utcnow() + timedelta(days=60),
                    application_deadline=datetime.utcnow() + timedelta(days=30),
                    description="Traditional Highland strength competition, divided into individual and team relay categories. The weight for the individual category is 50kg, and the total relay weight for the team category (3 members) is 120kg. Rankings are determined by completion time."
                )
            ]
            db.session.add_all(sample_competitions)

        db.session.commit()
    # --------------------------------------------------------------------------

    return app


# 导入模型（确保模型被识别，本地开发用）
from app.models import user, competition, application
