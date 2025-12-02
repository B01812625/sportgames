from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.auth.forms import RegistrationForm, LoginForm, DeleteAccountForm
from app.models.user import User
from app import db


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User Registration"""
    if current_user.is_authenticated:
        return redirect(url_for('competitions.list'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            consent_given=form.gdpr_consent.data
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please log in', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Sign Up', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User Login"""
    if current_user.is_authenticated:
        return redirect(url_for('competitions.list'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # Log in user (7 days remember me if checked)
            login_user(user, remember=form.remember.data, duration=3600 * 24 * 7)
            # Redirect to previously visited page (or competition list if none)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('competitions.list'))
        else:
            flash('Login failed! Invalid email or password', 'danger')

    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User Logout"""
    logout_user()
    flash('Successfully logged out', 'info')
    return redirect(url_for('competitions.list'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Profile Management"""
    return render_template('auth/profile.html', title='Profile')


@auth_bp.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    """Account Deletion (GDPR Compliance)"""
    form = DeleteAccountForm()
    if form.validate_on_submit():
        # Verify password
        if current_user.check_password(form.password.data):
            # Delete user (cascades to associated applications)
            db.session.delete(current_user)
            db.session.commit()
            flash('Account has been permanently deleted, and all associated data has been cleared', 'success')
            return redirect(url_for('competitions.list'))
        else:
            flash('Incorrect password, deletion failed', 'danger')

    return render_template('auth/delete_account.html', title='Delete Account', form=form)