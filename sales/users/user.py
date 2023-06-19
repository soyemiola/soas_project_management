from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from sales.users.forms import Login
from sales import baseURL, bcrypt
import requests
from sales.model import Users


user = Blueprint('user', __name__, url_prefix='/', template_folder='templates')

menu = 'dashboard'

@user.route('/soassales')
@user.route('/soassales/auth-login', methods=['POST', 'GET'])
def auth_login():
	if current_user.is_authenticated:
		return redirect(url_for('user.dashboard'))

	login = Login()

	if login.validate_on_submit():
		user_login = Users.query.filter_by(email=login.email.data).first()

		if user_login:
			if bcrypt.check_password_hash(user_login.password, login.password.data):
				login_user(user_login, remember=login.remember.data)
				next_page = request.args.get('next')

				return redirect(next_page) if next_page else redirect(url_for('user.dashboard'))
			else:
				flash('Sorry, Password is incorrect')

		else:
			det = response.json()
			flash(det['msg'], 'danger')	


	return render_template('users/auth-login.html', form=login)


@user.get('/soassales/auth-logout')
def auth_logout():
	logout_user()
	return redirect(url_for('user.auth_login'))



@user.get('/soassales/auth-forgot-password')
def auth_forgot_password():
	return render_template('users/auth-forgot-password.html')


@user.get('/soassales/dashboard')
@login_required
def dashboard():
	# client count
	# project count
	project_url = baseURL+''.join('/projects/list')
	# project list
	# actionable task
	# scouting list
	return render_template('users/dashboard.html', menu=menu)


@user.get('/soassales/users/profile/details')
@login_required
def profile(): 
	return render_template('users/profile.html', menu='profile')


@user.get('/soassales/users/profile/details/notification')
@login_required
def profile_notification():
	return render_template('users/profile_notification.html', menu='profile')

