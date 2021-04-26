from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField


class AddJobForm(FlaskForm):
    job = StringField('Название работы')
    team_leader = StringField('ID руководителя')
    work_size = StringField('Объем работы')
    collaborators = StringField('ID участников')
    is_finished = BooleanField('Работа закончена')
    submit = SubmitField('Добавить/Изменить')
