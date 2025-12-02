from flask import Blueprint

# 创建管理员蓝图
admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

from app.admin import routes