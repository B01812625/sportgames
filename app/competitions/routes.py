from flask import render_template, redirect, url_for, flash, request, current_app  # Import current_app
from flask_login import login_required, current_user
from app.competitions import comp_bp
from app.competitions.forms import ApplicationForm
from app.models.competition import Competition
from app.models.application import Application
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename


@comp_bp.route('/')
def list():
    """Competition List Page"""
    competitions = Competition.query.order_by(Competition.start_date).all()
    return render_template('competitions/list.html', title='Competition List', competitions=competitions)


@comp_bp.route('/<int:comp_id>')
def detail(comp_id):
    """Competition Detail Page"""
    competition = Competition.query.get_or_404(comp_id, description='This competition does not exist')
    return render_template('competitions/detail.html', title=competition.name, competition=competition)


@comp_bp.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    """Submit Competition Application"""
    form = ApplicationForm()
    # Dynamically load open competitions (deadline not passed)
    open_competitions = Competition.query.filter(Competition.application_deadline > datetime.utcnow()).order_by(
        Competition.start_date).all()
    form.competition_id.choices = [(comp.id, comp.name) for comp in open_competitions]

    if not open_competitions:
        flash('Currently, there are no open competitions for registration. Please stay tuned for updates', 'info')
        return redirect(url_for('competitions.list'))

    if form.validate_on_submit():
        comp_id = form.competition_id.data
        team_name = form.team_name.data.strip() or None

        # Check if user has already applied for this competition
        existing_app = Application.query.filter_by(
            user_id=current_user.id,
            competition_id=comp_id
        ).first()
        if existing_app:
            flash('You have already submitted an application for this competition. No need to reapply', 'warning')
            return redirect(url_for('competitions.detail', comp_id=comp_id))

        # Handle file upload (use current_app to get config instead of creating app instance directly)
        document_filename = None
        if form.document.data:
            # Secure filename handling
            filename = secure_filename(form.document.data.filename)
            # Get upload folder config from current_app (avoid circular import)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            # Create user-specific upload directory
            user_upload_dir = os.path.join(upload_folder, str(current_user.id))
            if not os.path.exists(user_upload_dir):
                os.makedirs(user_upload_dir)
            # Save file
            file_path = os.path.join(user_upload_dir, filename)
            form.document.data.save(file_path)
            document_filename = filename

        # Create competition application
        application = Application(
            user_id=current_user.id,
            competition_id=comp_id,
            team_name=team_name,
            document_filename=document_filename,
            notes=form.notes.data.strip()
        )
        db.session.add(application)
        db.session.commit()

        flash('Application submitted successfully! Please wait for admin review', 'success')
        return redirect(url_for('competitions.my_applications'))

    return render_template('competitions/apply.html', title='Submit Application', form=form)


@comp_bp.route('/my-applications')
@login_required
def my_applications():
    """My Competition Applications List"""
    applications = Application.query.filter_by(
        user_id=current_user.id
    ).join(Competition).order_by(Application.submission_date.desc()).all()
    return render_template('competitions/my_applications.html', title='My Applications', applications=applications)


@comp_bp.route('/application/<int:app_id>')
@login_required
def application_detail(app_id):
    """Competition Application Detail"""
    application = Application.query.filter_by(
        id=app_id, user_id=current_user.id
    ).join(Competition).first_or_404(description='This application does not exist')
    return render_template('competitions/application_detail.html', title='Application Detail', application=application)
