from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
import requests
from sales import baseURL
from sales import countries, get_country_from_ip


client = Blueprint('client', __name__, url_prefix='/', template_folder='templates')

menu = 'company'



@client.get('/soassales/client-list')
def client_list():
	try:
		url = baseURL+''.join('clients')
	
		clientlist = requests.get(url)
		
		if clientlist.status_code == 200:
			det = clientlist.json()
		else:
			det = None

	except Exception as e:
		flash('Error connecting to API host', 'danger')
		det = None

	return render_template('client/client_list.html', clients=det, menu=menu, submenu="cl")


@client.get('/soassales/client-add')
def client_add():
	client_ip = request.remote_addr
	
	#client_ip = '192.168.100.7'
	user_country = get_country_from_ip(client_ip)

	countrylist = countries()
	return render_template('client/client_add.html', user_country=user_country, countrylist=countrylist, menu=menu, submenu="nc")


@client.post('/soassales/client/client-save')
def save_client_record():
	if request.method == 'POST':

		try:
			data = {
				'clientname': request.form['clientname'],
				'country': request.form['country'],
				'state': request.form['state'],
				'address': request.form['address'],
				'email': request.form['email'],
				'number': request.form['number'],
				'industry': request.form['industry']
			}

			print(request.form['country'])

			url = baseURL+''.join('clients/add-client')
			print(url)

			response = requests.post(url, json=data)
			print(response)
			
			if response.status_code == 200:
				flash('New created successfully', 'success')
				return redirect(url_for('client.client_list'))
			else:
				flash('Error creating record. Try Again!', 'danger')
				return redirect(url_for('client.client_add'))

		except Exception as e:
			flash('Error saving details', 'danger')
			return redirect(url_for('client.client_add'))

	


@client.get('/soassales/client/<int:id>/client-edit')
def client_edit(id):
	return render_template('client/client_edit.html', menu=menu, submenu="cl") 


@client.patch('/soassales/client/<int:id>/client-update')
def client_update(id):
	return redirect(url_for('client.client_list')) 


@client.delete('/soassales/client/client-delete')
def client_delete():
	return redirect(url_for('client.client_list'))


@client.get('/soassales/client-contact-list')
def client_contact_list():
	url = baseURL+''.join('clients/contact-list')
	clientlist = requests.get(url)
	
	if clientlist.status_code == 200:
		det = clientlist.json()
	else:
		det = None
	return render_template('client/client_contact_list.html', det=det, menu=menu, submenu="ctl")


@client.get('/soassales/client-contact/add-record')
def client_contact_add():
	return render_template('client/client_contact_add.html', menu=menu, submenu="ctl")


@client.post('/soassales/client-contact/client-contact-save')
def save_client_contact_record():
	return redirect(url_for('client.client_contact_list'))


@client.get('/soassales/client-contact/<id>/edit-record')
def client_contact_edit(id):
	
	url = baseURL+''.join('clients/g-contact-list/'+id)
	contactsingle = requests.get(url)
	
	if contactsingle.status_code == 200:
		det = contactsingle.json()
	else:
		det = None

	return render_template('client/client_contact_edit.html', det=det, menu=menu, submenu="ctl")


@client.patch('/soassales/client/client-update')
def client_contact_update():
	return redirect(url_for('client.client_contact_list'))


@client.delete('/soassales/client/contact/contact-delete')
def client_contact_delete():
	return redirect(url_for('client.client_contact_list'))


@client.get('/soassales/client/scouting-list')
def scout_list():
	url = baseURL+''.join('clients/scout')
	scoutlist = requests.get(url)
	
	if scoutlist.status_code == 200:
		det = scoutlist.json()
	else:
		det = None

	return render_template('client/scout_list.html', det=det, menu=menu, submenu='sl')


@client.get('/soassales/client/scouting/add-record')
def add_scout():
	return render_template('client/add_scout.html', menu=menu, submenu='sl')


@client.post('/soassales/client/scouting/save-record')
def save_add_scout():
	return redirect(url_for('client.scout_list'))


@client.patch('/soassales/client/scouting/update-record')
def update_scout():
	return redirect(url_for('client.scout_list'))


@client.delete('/soassales/client/scouting/delete-record')
def delete_scout():
	return redirect(url_for('client.scout_list'))

