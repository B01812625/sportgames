from flask import Blueprint

# 创建赛事蓝图
comp_bp = Blueprint('competitions', __name__, template_folder='../templates/competitions')

from app.competitions import routes