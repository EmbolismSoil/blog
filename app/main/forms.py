from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import SubmitField


class NameForm(Form):
    name = StringField('what is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')