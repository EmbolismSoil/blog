from . import db
from flask_login import UserMixin, AnonymousUserMixin, login_manager
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime
import types

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
            db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(name='User').first()

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    views_count = db.Column(db.Integer, default=0, nullable=False)

    articles = db.relationship('Article', backref='user', lazy='dynamic')
    categories = db.relationship('Category', backref='user', lazy='dynamic')
    login_records = db.relationship('LoginRecord', backref='user', lazy='dynamic')

    @property
    def succeed_login_records(self):
        return list(filter(lambda r: r.status != 0, self.login_records))

    # 使用属性装饰器的方式实现属性的只读
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, password=pwd)

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def last_ip(self):
        return '0.0.0.0' if self.login_count <= 1 else self.succeed_login_records[1].ip

    @property
    def last_login(self):
        return datetime.utcnow() if self.login_count <= 1 else self.succeed_login_records[1].time

    @property
    def login_count(self):
        return len(self.succeed_login_records)

    @property
    def login_records_reversed(self):
        return self.login_records[:-10:-1]


class LoginRecord(db.Model):
    __tablename__ = 'login_record'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    ip = db.Column(db.String(128), default='0.0.0.0', nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    status = db.Column(db.Integer, nullable=False, default=0)

    @property
    def status_str(self):
        return '成功' if self.status else '失败'


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


class Article(db.Model):
    __tablename__ = 'articles'
    title = db.Column(db.String(128), unique=True)
    time = db.Column(db.DateTime(), default=datetime.utcnow, primary_key=True)
    comments = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    path = db.Column(db.String(512), nullable=False)
    #这里会定义索引吗？
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True)
    count = db.Column(db.Integer, default=0)
    articles = db.relationship('Article', backref='category', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
