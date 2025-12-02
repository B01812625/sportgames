from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models.competition import Competition

class CompetitionForm(FlaskForm):
    """Competition Creation/Edit Form"""
    name = StringField(
        'Competition Name',
        validators=[DataRequired(message='Competition name cannot be empty'), Length(max=100, message='Competition name must not exceed 100 characters')]
    )
    description = TextAreaField(
        'Competition Description',
        validators=[DataRequired(message='Competition description cannot be empty')]
    )
    category = SelectField(
        'Competition Category',
        validators=[DataRequired(message='Please select a competition category')],
        choices=[('Individual', 'Individual'), ('Team', 'Team'), ('Individual/Team', 'Individual/Team')]
    )
    start_date = DateTimeField(
        'Event Date',
        validators=[DataRequired(message='Please select an event date')],
        format='%Y-%m-%d %H:%M:%S',
        render_kw={'placeholder': 'Format: YYYY-MM-DD HH:MM:SS'}
    )
    application_deadline = DateTimeField(
        'Application Deadline',
        validators=[DataRequired(message='Please select an application deadline')],
        format='%Y-%m-%d %H:%M:%S',
        render_kw={'placeholder': 'Format: YYYY-MM-DD HH:MM:SS'}
    )
    submit = SubmitField('Save Competition')

class ApplicationReviewForm(FlaskForm):
    """Application Review Form"""
    status = SelectField(
        'Review Result',
        validators=[DataRequired(message='Please select a review result')],
        choices=[('approved', 'Approved'), ('rejected', 'Rejected')]
    )
    notes = TextAreaField(
        'Review Notes (Optional)',
        validators=[Length(max=500, message='Notes must not exceed 500 characters')]
    )
    submit = SubmitField('Submit Review')