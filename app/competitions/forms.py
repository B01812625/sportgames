from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  # Remove FileOptional
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional  # Import Optional from wtforms

# Allowed file extensions (replaces Flask-Uploads DOCUMENTS)
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'txt'}

class ApplicationForm(FlaskForm):
    """Competition Application Form"""
    competition_id = SelectField(
        'Competition Name',
        validators=[DataRequired(message='Please select a competition')],
        coerce=int  # Store as integer ID
    )
    team_name = StringField(
        'Team Name (Leave blank for individual applications)',
        validators=[Length(max=100, message='Team name must not exceed 100 characters')]
    )
    document = FileField(
        'Application Document (Optional, e.g., qualification certificate, team introduction)',
        validators=[
            Optional(),  # Use wtforms' Optional instead of FileOptional
            FileAllowed(ALLOWED_EXTENSIONS, message=f'Only the following formats are supported: {", ".join(ALLOWED_EXTENSIONS)}')
        ]
    )
    notes = TextAreaField(
        'Additional Notes (Optional)',
        validators=[Length(max=500, message='Notes must not exceed 500 characters')]
    )
    submit = SubmitField('Submit Application')