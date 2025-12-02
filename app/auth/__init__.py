from flask import Blueprint

# 创建认证蓝图
auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

from app.auth import routes