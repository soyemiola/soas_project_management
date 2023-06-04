from flask import Blueprint, render_template, redirect, url_for, request
import requests
from sales import baseURL


client = Blueprint('client', __name__, url_prefix='/', template_folder='templates')

menu = 'company'


@client.get('/soassales/v1/client-list')
def client_list():

	clients = requests.get(baseURL)
	
	return render_template('client/client_list.html', menu=menu, submenu="cl")


@client.get('/soassales/v1/client-add')
def client_add():
	return render_template('client/client_add.html', menu=menu, submenu="nc")


@client.post('/soassales/v1/client/client-save')
def save_client_record():
	return redirect(url_for('client.client_list'))


@client.get('/soassales/v1/client/<int:id>/client-edit')
def client_edit(id):
	return render_template('client/client_edit.html', menu=menu, submenu="cl") 


@client.patch('/soassales/v1/client/<int:id>/client-update')
def client_update(id):
	return redirect(url_for('client.client_list')) 


@client.delete('/soassales/v1/client/client-delete')
def client_delete():
	return redirect(url_for('client.client_list'))


@client.get('/soassales/v1/client-contact-list')
def client_contact_list():
	return render_template('client/client_contact_list.html', menu=menu, submenu="ctl")


@client.get('/soassales/v1/client-contact/add-record')
def client_contact_add():
	return render_template('client/client_contact_add.html', menu=menu, submenu="ctl")


@client.post('/soassales/v1/client-contact/client-contact-save')
def save_client_contact_record():
	return redirect(url_for('client.client_contact_list'))


@client.get('/soassales/v1/client-contact/<int:id>/edit-record')
def client_contact_edit(id):
	return render_template('client/client_contact_edit.html', menu=menu, submenu="ctl")


@client.patch('/soassales/v1/client/client-update')
def client_contact_update():
	return redirect(url_for('client.client_contact_list'))


@client.delete('/soassales/v1/client/contact/contact-delete')
def client_contact_delete():
	return redirect(url_for('client.client_contact_list'))


@client.get('/soassales/v1/client/scouting-list')
def scout_list():
	return render_template('client/scout_list.html', menu=menu, submenu='sl')


@client.get('/soassales/v1/client/scouting/add-record')
def add_scout():
	return render_template('client/add_scout.html', menu=menu, submenu='sl')


@client.post('/soassales/v1/client/scouting/save-record')
def save_add_scout():
	return redirect(url_for('client.scout_list'))


@client.patch('/soassales/v1/client/scouting/update-record')
def update_scout():
	return redirect(url_for('client.scout_list'))


@client.delete('/soassales/v1/client/scouting/delete-record')
def delete_scout():
	return redirect(url_for('client.scout_list'))