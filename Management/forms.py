from flask_wtf import Form
from wtforms import StringField
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), Email()])
    userpwd = PasswordField('密码', validators=[DataRequired()])

    def __init__(self):
        super().__init__(csrf_enabled=False)