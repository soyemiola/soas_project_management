from flask import Flask
from sales.config import Config
import os
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.blueprint_login_views = {'user': 'user.auth_login'}
login_manager.login_message_category = 'warning'


baseURL = 'http://localhost:5000/api/v1/'


def countries():
	file_path = os.path.join(os.path.dirname(__file__)+'\\static\\assets\\country.txt')
	
	try:
		with open(file_path, 'r') as file:
			country = file.read()
			file.close()
			return country
	except FileNotFoundError:
		return None



def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	
	db.init_app(app)
	login_manager.init_app(app)
	bcrypt.init_app(app)

	from sales.users.user import user
	from sales.users.team.member import member
	from sales.users.team.department import department
	from sales.users.clients.client import client
	from sales.users.project.project import project


	app.register_blueprint(user, url_prefix='/')
	app.register_blueprint(member, url_prefix='/')
	app.register_blueprint(department, url_prefix='/')
	app.register_blueprint(client, url_prefix='/')
	app.register_blueprint(project, url_prefix='/')


	return app

	