from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from app import bcrypt

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login required: Load user by ID"""
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    consent_given = db.Column(db.Boolean, nullable=False, default=False)  # GDPR consent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 双向关联：User ↔ Application
    applications = db.relationship(
        'Application',
        back_populates='user',  # 与 Application 模型的 user 属性双向绑定
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # Password property (not directly accessible)
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    # Set password with automatic encryption
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Verify password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} ({self.email})>'