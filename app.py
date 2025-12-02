from app import create_app, db
from app.models.user import User
from app.models.competition import Competition

app = create_app()

# 命令行：初始化数据库并添加测试数据
@app.cli.command("init-db")
def init_db():
    """初始化数据库并添加测试数据（管理员账号+示例赛事）"""
    db.create_all()
    print("数据库创建成功！")

    # 添加管理员账号（用户名：admin，密码：Admin123!，邮箱：admin@phg.com）
    if not User.query.filter_by(is_admin=True).first():
        admin = User(
            username='admin',
            email='admin@phg.com',
            password='Admin123!',  # 自动加密
            consent_given=True,
            is_admin=True
        )
        db.session.add(admin)
        print("管理员账号创建成功：")
        print("用户名：admin | 密码：Admin123! | 邮箱：admin@phg.com")

    # 添加示例赛事
    if not Competition.query.first():
        competitions = [
            Competition(
                name='高地舞蹈比赛',
                description='传统苏格兰高地舞蹈竞赛，分为单人组和双人组，需按照传统舞步表演',
                category='个人/团队',
                start_date='2025-08-15 10:00:00',
                application_deadline='2025-07-30 23:59:59'
            ),
            Competition(
                name='苏格兰风笛演奏',
                description='风笛独奏或合奏比赛，曲目需包含传统苏格兰民谣',
                category='个人/团队',
                start_date='2025-08-16 09:30:00',
                application_deadline='2025-08-05 23:59:59'
            ),
            Competition(
                name='高地举重挑战赛',
                description='传统高地力量竞赛，包含石球投掷、木杆举重等项目',
                category='个人',
                start_date='2025-08-17 14:00:00',
                application_deadline='2025-08-10 23:59:59'
            )
        ]
        db.session.add_all(competitions)
        print("3个示例赛事添加成功！")

    db.session.commit()
    print("初始化完成！")

if __name__ == '__main__':
    app.run(debug=True)