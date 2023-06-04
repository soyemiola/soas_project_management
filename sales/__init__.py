from flask import Flask
from sales.config import Config


baseURL = 'http://localhost:5000'

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

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

	