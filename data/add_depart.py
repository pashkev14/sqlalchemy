from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import EmailField


class AddDepartForm(FlaskForm):
    title = StringField('Название департамента')
    chief = StringField('ID руководителя')
    members = StringField('ID членов')
    email = EmailField('Адрес электронной почты')
    submit = SubmitField('Добавить/Изменить')
