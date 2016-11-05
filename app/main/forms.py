from flask_wtf import Form
from wtforms import StringField, FileField, SelectField
from wtforms.validators import DataRequired
from wtforms import SubmitField


class NameForm(Form):
    name = StringField('what is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ArticleForm(Form):
    category = SelectField(u'Group')
    title = StringField('Title', validators=[DataRequired()])
    path = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')


class CategoryForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')