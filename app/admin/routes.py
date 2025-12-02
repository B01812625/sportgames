from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.admin import admin_bp
from app.admin.forms import CompetitionForm, ApplicationReviewForm
from app.models.user import User
from app.models.competition import Competition
from app.models.application import Application
from app import db
from datetime import datetime  # 导入datetime模块
import os
from functools import wraps


# 管理员权限装饰器（确保只有管理员能访问）
def admin_required(f):
    @wraps(f)  # 关键：保留原函数名称，避免端点冲突
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have administrator privileges to access this page', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function


@admin_bp.route('/dashboard', endpoint='dashboard')  # 显式指定 endpoint
@login_required
@admin_required
def dashboard():
    """管理员仪表盘"""
    # 统计数据
    total_users = User.query.count()
    total_competitions = Competition.query.count()
    total_applications = Application.query.count()
    pending_applications = Application.query.filter_by(status='pending').count()
    approved_applications = Application.query.filter_by(status='approved').count()
    rejected_applications = Application.query.filter_by(status='rejected').count()

    # 近期赛事（未来3个）- 移到路由中查询，避免模板直接操作模型
    upcoming_competitions = Competition.query.filter(
        Competition.start_date > datetime.utcnow()
    ).order_by(Competition.start_date).limit(3).all()

    # 待审核申请（最新3个）- 关联User和Competition，确保app.user和app.competition可访问
    pending_apps = Application.query.filter_by(status='pending').join(
        User
    ).join(
        Competition
    ).order_by(Application.submission_date.desc()).limit(3).all()

    # 传递Competition模型和datetime到模板（解决UndefinedError）
    return render_template(
        'admin/dashboard.html',
        title='Admin Dashboard',
        total_users=total_users,
        total_competitions=total_competitions,
        total_applications=total_applications,
        pending_applications=pending_applications,
        approved_applications=approved_applications,
        rejected_applications=rejected_applications,
        upcoming_competitions=upcoming_competitions,
        pending_apps=pending_apps,
        Competition=Competition,
        datetime=datetime
    )


@admin_bp.route('/competitions', endpoint='competition_list')  # 显式指定 endpoint
@login_required
@admin_required
def competition_list():
    """赛事管理列表"""
    competitions = Competition.query.order_by(Competition.start_date.desc()).all()
    return render_template('admin/competition_list.html', title='Competition Management', competitions=competitions)


@admin_bp.route('/competitions/create', methods=['GET', 'POST'], endpoint='create_competition')  # 显式指定 endpoint
@login_required
@admin_required
def create_competition():
    """创建新赛事"""
    form = CompetitionForm()
    if form.validate_on_submit():
        competition = Competition(
            name=form.name.data.strip(),
            category=form.category.data,
            start_date=form.start_date.data,
            application_deadline=form.application_deadline.data,
            description=form.description.data.strip()
        )
        db.session.add(competition)
        db.session.commit()
        flash(f'Competition "{competition.name}" created successfully!', 'success')
        return redirect(url_for('admin.competition_list'))
    return render_template('admin/competition_form.html', title='Create New Competition', form=form)


@admin_bp.route('/competitions/<int:comp_id>/edit', methods=['GET', 'POST'],
                endpoint='edit_competition')  # 显式指定 endpoint
@login_required
@admin_required
def edit_competition(comp_id):
    """编辑赛事"""
    competition = Competition.query.get_or_404(comp_id, description='This competition does not exist')
    form = CompetitionForm(obj=competition)
    if form.validate_on_submit():
        competition.name = form.name.data.strip()
        competition.category = form.category.data
        competition.start_date = form.start_date.data
        competition.application_deadline = form.application_deadline.data
        competition.description = form.description.data.strip()
        db.session.commit()
        flash(f'Competition "{competition.name}" updated successfully!', 'success')
        return redirect(url_for('admin.competition_list'))
    return render_template('admin/competition_form.html', title=f'Edit Competition: {competition.name}', form=form,
                           competition=competition)


@admin_bp.route('/competitions/<int:comp_id>/delete', methods=['POST'], endpoint='delete_competition')  # 显式指定 endpoint
@login_required
@admin_required
def delete_competition(comp_id):
    """删除赛事"""
    competition = Competition.query.get_or_404(comp_id, description='This competition does not exist')
    # 删除赛事关联的所有申请（级联删除）
    applications = Application.query.filter_by(competition_id=comp_id).all()
    for app in applications:
        # 删除关联的上传文件
        if app.document_filename:
            user_upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(app.user_id))
            file_path = os.path.join(user_upload_dir, app.document_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        db.session.delete(app)
    # 删除赛事
    db.session.delete(competition)
    db.session.commit()
    flash(f'Competition "{competition.name}" has been deleted (including associated applications and files)', 'success')
    return redirect(url_for('admin.competition_list'))


@admin_bp.route('/applications', endpoint='application_list')  # 显式指定 endpoint
@login_required
@admin_required
def application_list():
    """参赛申请管理列表"""
    status = request.args.get('status', 'all')
    query = Application.query.join(User).join(Competition)  # 先join User，再join Competition
    if status == 'pending':
        applications = query.filter(Application.status =='pending').order_by(Application.submission_date.desc()).all()
    elif status == 'approved':
        applications = query.filter(Application.status =='approved').order_by(Application.submission_date.desc()).all()
    elif status == 'rejected':
        applications = query.filter(Application.status =='rejected').order_by(Application.submission_date.desc()).all()
    else:
        applications = query.order_by(Application.submission_date.desc()).all()
    return render_template('admin/application_list.html', title='Application Management', applications=applications,
                           current_status=status)


@admin_bp.route('/applications/<int:app_id>/review', methods=['GET', 'POST'],
                endpoint='review_application')  # 显式指定 endpoint
@login_required
@admin_required
def review_application(app_id):
    """审核参赛申请"""
    application = Application.query.get_or_404(app_id, description='This application does not exist')
    form = ApplicationReviewForm(obj=application)
    if form.validate_on_submit():
        application.status = form.status.data
        application.notes = form.notes.data.strip()
        application.approved_at = datetime.utcnow()
        db.session.commit()
        flash(f'Application review status updated to "{application.status}"', 'success')
        return redirect(url_for('admin.application_list', status=application.status))
    return render_template('admin/review_application.html', title='Review Application', form=form, application=application)