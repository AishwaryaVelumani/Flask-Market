from flask import Flask #render_templates helps to route to the html files
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#import os
#from market.config import DEV_DB, PROD_DB

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY']='aee8450d7c89cce43cc44e8b'
db=SQLAlchemy(app) #creates instance of sqlalchemy db
bcrypt =Bcrypt(app)
login_manager= LoginManager(app)
login_manager.login_view= "login_page" #used by login_required to get the users to login before the accessing market page
login_manager.login_message_category="info"
from market import routes
#init file is the first file that is executed when a package is used.
#always present in every package
#when u import a file python will try to execute that file


