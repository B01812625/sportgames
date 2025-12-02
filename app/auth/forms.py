from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.user import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(message='Username cannot be empty'),
                                       Length(min=2, max=20, message='Username must be between 2 and 20 characters')])
    email = StringField('Email',
                        validators=[DataRequired(message='Email cannot be empty'),
                                    Email(message='Please enter a valid email address')])
    password = PasswordField('Password',
                             validators=[DataRequired(message='Password cannot be empty'),
                                         Length(min=6, message='Password must be at least 6 characters long')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message='Please confirm your password'),
                                                 EqualTo('password', message='Passwords do not match')])
    # Plain text label without url_for
    gdpr_consent = BooleanField(
        'I have read and agree to the Privacy Policy, and consent to the collection and use of my personal data in compliance with GDPR requirements',
        validators=[DataRequired(message='You must agree to the Privacy Policy to register')]
    )
    submit = SubmitField('Sign Up')

    # Username duplication validation
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose another one.')

    # Email duplication validation
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please use another one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message='Email cannot be empty'),
                                    Email(message='Please enter a valid email address')])
    password = PasswordField('Password',
                             validators=[DataRequired(message='Password cannot be empty')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class DeleteAccountForm(FlaskForm):
    """Account Deletion Form (for GDPR compliance)"""
    password = PasswordField('Enter Password to Confirm',
                             validators=[DataRequired(message='Please enter your password to confirm')])
    submit = SubmitField('Confirm Account Deletion')