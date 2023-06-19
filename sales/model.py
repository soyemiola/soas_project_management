from flask import session, current_app, session
from sales import db, login_manager
from flask_login import UserMixin


	
@login_manager.user_loader
def load_user(user_id):
	user = Users.query.get(int(user_id))
	return user
	


class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	fullname = db.Column(db.String(255))
	organization = db.Column(db.String(255))
	department = db.Column(db.String(255))
	email = db.Column(db.String(255))
	number = db.Column(db.Integer)
	role = db.Column(db.Integer)
	status = db.Column(db.String(255))
	password = db.Column(db.Text)
	img = db.Column(db.Text)


	def __repr__(self):
		return f'User Info: {self.id}, {self.fullname}, {self.organization}, {self.department}, {self.email}, \
				{self.number}, {self.role}, {self.status}, {self.img}'


