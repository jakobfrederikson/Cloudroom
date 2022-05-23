from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# file location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloudroom.db'
app.config['SECRET_KEY'] = '40cbeb3aa5d35a97424d230b'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "sign_in"
login_manager.login_message_category = "info"

from CloudMain import route