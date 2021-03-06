from flask import Flask, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import redirect
from data import db_session
from data.add_job import AddJobForm
from data.log import LoginForm
from data.__all_models import *
from data.reg import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/jobs.db")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def base():
    if current_user.is_authenticated:
        return redirect('/log')
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    css = url_for('static', filename='css/base.css')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/log")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form, css=css)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    css = url_for('static', filename='css/base.css')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", css=css)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", css=css)
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, css=css)


@app.route('/log')
@login_required
def show_db():
    db_session.global_init("db/jobs.db")
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs)
    css = url_for('static', filename='css/base.css')
    return render_template("index.html", css=css, jobs=jobs)


@app.route('/addjob',  methods=['GET', 'POST'])
@login_required
def add_job():
    css = url_for('static', filename='css/base.css')
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/log')
    return render_template('addjob.html', form=form, css=css)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1', debug=True)
