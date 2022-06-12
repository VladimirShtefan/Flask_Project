from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///service_db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super secret key"
db = SQLAlchemy(app)

manager = LoginManager(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(25), nullable=False)


@manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('user_name')
    password = request.form.get('user_password')
    if name and password:
        print(name, password)
        user = User.query.filter_by(login=name).first()
        print(user)
        if check_password_hash(user.password, password):
            login_user(user)
            # next_page = request.args.get('next')
            redirect(url_for('objects'))
        else:
            flash('Не верный логин или пароль')
            # return render_template(url_for('objects'))
    else:
        flash('Не заполнены поля логин/пароль')
        return render_template(url_for('index'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass


@app.route('/objects', methods=['GET'])
def objects():
    return render_template('objects.html')
