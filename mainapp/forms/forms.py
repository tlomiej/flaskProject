from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    form = TextAreaField('Form', validators=[DataRequired()])

    submit = SubmitField('Create')
