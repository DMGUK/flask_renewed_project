from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ToDoForm(FlaskForm):
    title = StringField('Todo Title', validators=[DataRequired("This field is required"), Length(min=1, max=100)])
    description = StringField('', validators=[DataRequired("This field is required"), Length(min=1 , max=200)])
    submit = SubmitField("Add new task")