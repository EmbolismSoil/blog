#
from flask import render_template, request, flash
from . import main
from ..models import Article
from .forms import ArticleForm, CategoryForm
from flask_login import login_required
from app import db
from flask_login import current_user
from ..models import User
from ..models import Category
from flask import url_for, redirect
from datetime import datetime
from markdown import markdown


@main.route('/', methods=['GET', 'POST'])
def index():
    user = User.query.filter_by(username='LEEK').first()
    user.article_count = user.articles.count()
    user.comment_count = 0
    user.category_count = user.categories.count()
    user.like_count = 0
    user.views_count = 0

    for article in user.articles:
        user.comment_count += article.comments
        user.like_count += article.likes
        user.views_count += article.views

    return render_template('new_index_template.html', user=user)


@main.route('/post-preview')
def get_post_preview():
    offset = request.args.get('offset')
    count = request.args.get('count')
    articles = Article.query.order_by(Article.time.desc()).offset(offset).limit(count).all()
    now = datetime.utcnow()
    for article in articles:
        article.html_path = article.path
        if round((now - article.time).days) > 0:
            article.time_diff = str(round((now - article.time).days)) + ' 天之前'
        elif round((now - article.time).seconds / 3600) > 0:
            article.time_diff = str(round((now - article.time).seconds / 3600)) + ' 小时前'
        elif round((now - article.time).seconds / 60) > 0:
            article.time_diff = str(round((now - article.time).seconds / 60)) + ' 分钟前'
        else:
            article.time_diff = str(round((now - article.time).seconds)) + ' 秒之前'

    return render_template('article-list.html', articles=articles)


@main.route('/view/article')
def view_article():
    path = request.args.get('path')
    if path is None:
        return redirect(url_for('main.index'))
    return render_template('view_article.html', path=path)


@main.route('/editor')
def editor():
    return render_template('editor.html');


@main.route('/test/')
def test_index():
    return render_template('new_index.html')


@main.route('/add-article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm()
    categories = Category.query.all()

    if categories is None:
        return redirect(url_for('main.add_category'))

    choices = []
    for item in categories:
        choices.append((item.name, item.name))

    form.category.choices = choices

    if form.validate_on_submit():
        file = form.path.data
        preview_path = '/static/markdown/' + datetime.now().strftime('%Y-%m-%d') + '-' + file.filename
        path = 'app' + preview_path
        article = Article(title=form.title.data, path=path)
        article.path = preview_path
        article.user_id = current_user.id
        c = Category.query.filter_by(name=form.category.data).first()
        cid = c.id
        article.category_id = cid
        c.count += 1
        db.session.add(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Upload failed')
        else:
            file.save(path)
            file = open(path, 'r')
            all_text = file.read()
            print(all_text)
            html_text = markdown(all_text, format="html")
            html_file = open(path + ".html", 'w')
            html_file.writelines(html_text)
            html_file.close()
            flash('Upload successfully')

    return render_template('add-article.html', form=form)


@main.route('/add-category', methods=['POST', 'GET'])
@login_required
def add_category():
    form = CategoryForm()

    if form.validate_on_submit():
        category = Category(name=form.name.data, user_id=current_user.id, count=0)
        db.session.add(category)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('Add category failed')
        else:
            flash('Add category successfully')

    return render_template('add-category.html', form=form)