from app import db
from datetime import datetime

class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)  # Foreign key to Competition
    team_name = db.Column(db.String(100), nullable=True)  # Team name (leave blank for individual)
    document_filename = db.Column(db.String(255), nullable=True)  # Uploaded file name
    notes = db.Column(db.Text, nullable=True)  # Additional notes
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending/approved/rejected
    submission_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  # Submission time
    approved_at = db.Column(db.DateTime, nullable=True)  # Review time

    # 双向关联：Application ↔ User（与 User.applications 双向绑定）
    user = db.relationship(
        'User',
        back_populates='applications',  # 对应 User 模型的 applications 属性
        lazy=True
    )

    # 双向关联：Application ↔ Competition（与 Competition.applications 双向绑定）
    competition = db.relationship(
        'Competition',
        back_populates='applications',  # 对应 Competition 模型的 applications 属性
        lazy=True
    )

    def __repr__(self):
        # 确保关联属性存在后再访问（避免初始化时报错）
        username = self.user.username if self.user else 'Unknown User'
        comp_name = self.competition.name if self.competition else 'Unknown Competition'
        return f'<Application {self.id} - {username} - {comp_name}>'