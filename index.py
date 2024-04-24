from flask import Flask, render_template, redirect, request, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
import os
from cf_api import create_json
from excel_table import new_excel_table
import json

global us
global jsonData
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def home_page():
    global us
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        us = db_sess.query(User).where(User.name == current_user.name).first().name
    return render_template('index.html', title='Home Page')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/new_table', methods=['GET', 'POST'])
@login_required
def new_table():
    global us
    global jsonData
    create_json(us)
    with open(f'json/{us}_contest.json', 'r') as f:
        jsonData = json.load(f)
    return render_template('table.html', jsonData=jsonData, title='Новая таблица')


@app.route('/download_file')
@login_required
def u():
    global path
    return send_file(path, as_attachment=True)


@app.route('/submit', methods=['POST'])
@login_required
def submit():
    global jsonData
    global path
    submit_tup = []
    if request.method == 'POST':
        checkbox_items = request.form.getlist('checkboxItem')
        for item in checkbox_items:
            submit_tup.append((item, f'https://codeforces.com{jsonData[item]}/standings/groupmates/true'))
        print(submit_tup)
        path = new_excel_table(submit_tup, us)
        return render_template('submit.html')


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host="127.0.0.1")


if __name__ == '__main__':
    main()
