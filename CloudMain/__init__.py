from flask import Flask, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_mobility import Mobility

ckeditor = CKEditor()
app = Flask(__name__)
# file location
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "cloudroomproject203@gmail.com"
app.config['MAIL_PASSWORD'] = ""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloudroom.db'
app.config['SECRET_KEY'] = '40cbeb3aa5d35a97424d230b'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page" #redirect user to login page if they are not signed in
login_manager.login_message_category = "info"
ckeditor.init_app(app)
mail = Mail(app)
mobility = Mobility(app) # This allows us to check if the user is on mobile or not

from CloudMain import route
