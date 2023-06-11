from flask import Blueprint, render_template


user = Blueprint('user', __name__, url_prefix='/', template_folder='templates')

menu = 'dashboard'

@user.get('/soassales')
@user.get('/soassales/auth-login')
def auth_login():
	return render_template('users/auth-login.html')


@user.get('/soassales/auth-forgot-password')
def auth_forgot_password():
	return render_template('users/auth-forgot-password.html')


@user.get('/soassales/dashboard')
def dashboard():
	return render_template('users/dashboard.html', menu=menu)


@user.get('/soassales/users/profile/details')
def profile():
	return render_template('users/profile.html', menu='profile')

@user.get('/soassales/users/profile/details/notification')
def profile_notification():
	return render_template('users/profile_notification.html', menu='profile') 