from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from openai_logic import process_headings, input_keywords, input_headers, unique_text
from dotenv import load_dotenv
import os
from flask_admin import Admin, form, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView

# load the .env file
load_dotenv()

# configurate the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# configuring the database
db.init_app(app)
with app.app_context():
        db.create_all()  # Создание базы данных

        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            new_admin = User(username='admin', password=os.environ.get(
                'ADMIN_PASSWD'), is_admin=True)
            db.session.add(new_admin)
            db.session.commit()


# configurate the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize your admin with a custom index view
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

# configuring the admin panel
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3', index_view=MyAdminIndexView())

# class for accesibility to the admin panel
class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('generate'))


# add the access to the admin
admin.add_view(UserModelView(User, db.session))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('generate'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(
            username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('generate'))
        flash('Invalid username or password')
    return render_template('login_form.html')


@app.route('/generate', methods=['GET', 'POST'])
@login_required
def generate():
    if request.method == 'POST':
        headers = request.form['headers']
        keywords = request.form['keywords']
        print(headers, keywords)
        return send_file(process_headings(input_headers(headers), input_keywords(keywords)))

    return render_template('index.html', is_admin=current_user.is_admin)


@app.route('/uniq', methods=['GET', 'POST'])
@login_required
def uniq():
    if request.method == 'POST':
        user_text = request.form['user-text']
        return render_template('result.html', result=unique_text(user_text))

    return render_template('uniq.html', is_admin=current_user.is_admin)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    

    app.run(debug=True)
