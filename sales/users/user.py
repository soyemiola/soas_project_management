from flask import Blueprint, render_template


user = Blueprint('user', __name__, url_prefix='/', template_folder='templates')

menu = 'dashboard'


@user.get('/soassales/v1/auth-login')
def auth_login():
	return render_template('users/auth-login.html')


@user.get('/soassales/v1/auth-forgot-password')
def auth_forgot_password():
	return render_template('users/auth-forgot-password.html')


@user.get('/soassales/v1/dashboard')
def dashboard():
	return render_template('users/dashboard.html', menu=menu)


@user.get('/soassales/v1/users/profile/details')
def profile():
	return render_template('users/profile.html', menu='profile')

@user.get('/soassales/v1/users/profile/details/notification')
def profile_notification():
	return render_template('users/profile_notification.html', menu='profile')