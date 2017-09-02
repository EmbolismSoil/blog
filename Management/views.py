from . import management
from flask import render_template, flash, \
    redirect, request, url_for, make_response, \
    current_app, abort, session

from .forms import LoginForm
from app.models import db, Role, Article, Category
from flask_login import login_user, current_user, logout_user
from app.models import User, LoginRecord
from .utils import admin_required
from platform import platform, python_version
import time



@management.route('/', methods=['GET'])
@admin_required
def management_index():
    admin_count = Role.query.filter_by(name='Administrator').limit(1).first().users.count()
    eng = db.get_engine(current_app)
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    ts = time.time()
    ret = render_template('management-system/index.html',
                           user=current_user, admin_count=admin_count, now=now,
                           platform=platform(), python_version=python_version(),
                           remote_addr=request.remote_addr,
                           db_version=eng.dialect.server_version_info,
                           render_time=lambda: round(time.time() - ts, 2)
                          )
    return ret


@management.route('/login', methods=['GET', 'POST'])
def management_login():
    if current_user.is_authenticated:
        if current_user.is_administrator():
            return redirect(url_for('management.management_index'))
        else:
            flash('非系统管理员账号已登录，现已自动退出，请重新登录')
            logout_user()
            return redirect(url_for('management.management_login'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.username.data).first()
        if user is not None:
            login_record = LoginRecord(status=0, user_id=user.id, ip=request.remote_addr)
            if not user.verify_password(form.userpwd.data):
                flash('用户名或密码错误')
                db.session.add(login_record)
                db.session.commit()
                return render_template('management-system/login.html')

            if not user.is_administrator():
                flash('非系统管理员账号')
                db.session.add(login_record)
                db.session.commit()
                return render_template('management-system/login.html')
            else:
                login_user(user, True)
                login_record.status = 1
                db.session.add(login_record)
                db.session.commit()
                return redirect(request.args.get('next') or url_for('management.management_index'))
        else:
            flash('用户名或密码错误')

    return render_template('management-system/login.html')


@management.route('/article/page/<int:page>', methods=['GET'])
@admin_required
def article_page(page):
    article_count = Article.query.filter_by(user_id=current_user.id).count()
    pages = (article_count + 6) // 7

    if page > pages:
        return abort(404)

    articles = Article.query.filter_by(user_id=current_user.id).limit(7).offset((page - 1) * 7)

    if articles is None:
        articles = []
        return render_template('management-system/article.html',
                               user=current_user, articles=articles)

    articles_info = []
    for article in articles:
        category = Category.query.filter_by(id=article.category_id).first()
        articles_info.append({'title': article.title,
                              'category': category.name,
                              'comment_count': article.comments,
                              'date': article.time.strftime('%Y-%m-%d')
                              })

    session['cur_page'] = page
    return render_template('management-system/article.html',
                           user=current_user, articles=articles_info, cur_page=page, pages=pages)


@management.route('/article/')
@admin_required
def article():
    page = 1
    if 'cur_page' in session:
        page = session['cur_page']

    return redirect(url_for('management.article_page', page=page))


@management.route('/logout', methods=['GET'])
@admin_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('management.management_index'))


@management.route('/ping', methods=['GET'])
@admin_required
def ping():
    return make_response()

