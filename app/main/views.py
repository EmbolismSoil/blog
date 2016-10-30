#
from flask import render_template
from . import main
from app.models import User
from flask import abort, flash, redirect, url_for
from flask_login import login_required, current_user
from ..auth.forms import EditProfileForm, EditProfileAdminForm
from app.models import db
from app.decorators import admin_required
from .markdown import Markdown
from markdown import markdown


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        return abort(404)
    return render_template('user.html', user=u)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been update')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = form.role.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been update')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit-profile.html', form=form, user=user)


@main.route('/post-preview', methods=['GET'])
def get_post_preview():
    md = Markdown('app/static/markdown/effective_python.md')
    md.img_url = '/static/post-1.jpg'
    return render_template('preview.html', article=md)


@main.route('/view/article/<name>')
def view_article(name):
    return render_template('view_article.html', name=name)