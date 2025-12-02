from app import db
from datetime import datetime

class Competition(db.Model):
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Individual/Team/Mixed
    start_date = db.Column(db.DateTime, nullable=False)
    application_deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 双向关联：Competition ↔ Application
    applications = db.relationship(
        'Application',
        back_populates='competition',  # 与 Application 模型的 competition 属性双向绑定
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # Check if registration is open (deadline not passed)
    @property
    def is_open_for_application(self):
        return datetime.utcnow() < self.application_deadline

    def __repr__(self):
        return f'<Competition {self.name}>'