from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SECRET_KEY'] = 'Secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Todo(db.Model):
    todoid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, unique=False)
    title = db.Column(db.String(130), unique=False)
    status = db.Column(db.String(20), unique=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Password"})
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(
        message="Invalid Email"), Length(max=50)], render_kw={"placeholder": "Email Address"})
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=15)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", validators=[InputRequired(), Length(
        min=4, max=50)], render_kw={"placeholder": "Password"})

class CreateForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(
        min=2, max=130)], render_kw={"placeholder": "Enter a task"})
    status = RadioField('Status', choices=[('todo', 'To Do'), ('doing', 'Doing'), ('done', 'Done')], validators=[InputRequired()])


@app.route('/', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def index():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account was successfully created! You are able to login now.')
        return redirect(url_for('login'))

    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login successful!')
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    todo = Todo.query.filter_by(status="todo", id=current_user.id).all()
    doing = Todo.query.filter_by(status="doing", id=current_user.id).all()
    done = Todo.query.filter_by(status="done", id=current_user.id).all()
    return render_template('dashboard.html', username = current_user.username, todo=todo, doing=doing, done=done)

@app.route('/addtodo', methods=['GET', 'POST'])
@login_required
def addtodo():
    form = CreateForm(request.form)
    if form.validate_on_submit():

        new_todo = Todo(id=current_user.id, title=form.title.data, status=form.status.data)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('addtodo.html', form=form)

@app.route('/doing/<todoid>', methods=['GET','POST'])
def doing(todoid):
    todo = Todo.query.filter_by(todoid=int(todoid)).first()
    todo.status = 'doing'
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/done/<todoid>', methods=['GET','POST'])
def done(todoid):
    todo = Todo.query.filter_by(todoid=int(todoid)).first()
    todo.status = 'done'
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/delete/<todoid>', methods=['GET','POST'])
def delete(todoid):
    deleted = Todo.query.filter_by(todoid=int(todoid)).first()
    db.session.delete(deleted)
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()