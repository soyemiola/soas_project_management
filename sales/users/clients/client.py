from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
import requests
from sales import baseURL
from sales import countries


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
	cl = countries()
	countrylist = cl.split(',')

	return render_template('client/client_add.html', user_country=countrylist, countrylist=countrylist, menu=menu, submenu="nc")


@client.post('/soassales/client/client-save')
def save_client_record():
	if request.method == 'POST':
		createdby = 1 # current_user_id
		try:
			data = {
				'clientname': request.form['clientname'],
				'country': request.form['country'],
				'state': request.form['state'],
				'address': request.form['address'],
				'email': request.form['email'],
				'number': request.form['number'],
				'industry': request.form['industry'],
				'createdby': createdby,
				'contact': request.form.getlist('crdt_contact')
			}

			url = baseURL+''.join('clients/add-client')

			response = requests.post(url, json=data)
			
			if response.status_code == 200:
				flash('New created successfully', 'primary')
				return redirect(url_for('client.client_list'))
			else:
				flash('Error creating record. Try Again!', 'danger')
				return redirect(url_for('client.client_add'))

		except Exception as e:
			flash('Error saving details', 'danger')
			return redirect(url_for('client.client_add'))

	
@client.get('/soassales/client/<int:id>/client-edit')
def client_edit(id):
	cl = countries()
	countrylist = cl.split(',')

	try:
		url = baseURL+''.join(f'clients/one/{id}')
	
		clientlist = requests.get(url)
		
		if clientlist.status_code == 200:
			det = clientlist.json()
		else:
			det = None

	except Exception as e:
		flash('Error connecting to API host', 'danger')
		det = None

	return render_template('client/client_edit.html', user_country=countrylist, det=det, menu=menu, submenu="cl") 


@client.patch('/soassales/client/client-update')
def client_update(id):
	if request.method == 'POST':
		
		try:
			data = {
				'id': request.form['id'],
				'clientname': request.form['clientname'],
				'country': request.form['country'],
				'state': request.form['state'],
				'address': request.form['address'],
				'email': request.form['email'],
				'number': request.form['number'],
				'industry': request.form['industry'],
				'status': request.form['status']
			}

			url = baseURL+''.join('clients/update')

			response = requests.patch(url, json=data)
			
			if response.status_code == 200:
				flash('Profile updated', 'primary')
				return redirect(url_for('client.client_list'))
			else:
				flash('Error updating record. Try Again!', 'danger')
				return redirect(url_for('client.client_add'))

		except Exception as e:
			flash('Error saving details', 'danger')
			return redirect(url_for('client.client_add'))
	return redirect(url_for('client.client_list')) 


@client.delete('/soassales/client/client-delete')
def client_delete():
	return redirect(url_for('client.client_list'))


@client.get('/soassales/client-contact-list')
def client_contact_list():
	try:
		url = baseURL+''.join('contacts')
		res = requests.get(url)

		if res.status_code == 200:
			det = res.json()
		else:
			det = None
	except Exception as e:
		det = None
		flash(e, "danger")

	return render_template('client/client_contact_list.html', det=det, menu=menu, submenu="ctl")


@client.get('/soassales/client-contact/add-record')
def client_contact_add():
	try:
		url = baseURL+''.join('clients')
		getclients = requests.get(url)

		if getclients.status_code == 200:
			clients = getclients.json()
		else:
			clients = None
	except Exception as e:
		flash(e, "danger")
		clients = None

	return render_template('client/client_contact_add.html', clients=clients, menu=menu, submenu="ctl")


@client.post('/soassales/client-contact/client-contact-save')
def save_client_contact_record():
	if request.method == 'POST':
		try:
			current_user = 1
			data = {
				"company": request.form['company'],
				"name": request.form['name'],
				"email": request.form['email'],
				"position": request.form['position'],
				"number": request.form['number'],
				"createdby": current_user
			}

			url = baseURL+''.join('contacts/add')
			
			save = requests.post(url, json=data)

			if save.status_code == 200:
				flash("New record created!", "primary")
			else:
				det = save.json()
				flash(det['msg'], "danger")
			
			return redirect(url_for("client.client_contact_add"))

		except Exception as e:
			flash(e, "danger")
			return redirect(url_for("client.client_contact_add"))


@client.get('/soassales/client-contact/<id>/edit-record')
def client_contact_edit(id):
	
	url = baseURL+''.join(f'contacts/one/{id}')
	getdet = requests.get(url)

	curl = baseURL+''.join('clients')
	getclients = requests.get(curl)

	if getdet.status_code == 200:
		det = getdet.json()
		clients = getclients.json()
	else:
		det = getdet.json()
		flash(det['msg'], "danger")

	return render_template('client/client_contact_edit.html', det=det, clients=clients, menu=menu, submenu="ctl")


@client.post('/soassales/client/client-update')
def client_contact_update():
	if request.method == 'POST':
		try:
			data = {
				"id": request.form['id'],
				"company": request.form['company'],
				"name": request.form['name'],
				"email": request.form['email'],
				"position": request.form['position'],
				"number": request.form['number'],
				"status": request.form['status']
			}

			url = baseURL+''.join('contacts/update')
			
			save = requests.patch(url, json=data)

			if save.status_code == 200:
				flash("Record updated", "primary")
			else:
				det = save.json()
				flash(det['msg'], "danger")
			
			return redirect(url_for("client.client_contact_edit", id=data['id']))

		except Exception as e:
			flash(e, "danger")
			return redirect(url_for("client.client_contact_list", ))


@client.post('/soassales/client/contact/contact-delete')
def client_contact_delete():
	id = request.form['id']
	url = baseURL+''.join(f'contacts/delete/{id}')

	delete = requests.delete(url)
	if delete.status_code == 200:
		det = delete.json()

		flash(det['msg'], 'primary')
	else:
		det = delete.json()
		flash(det['msg'], 'danger')

	return redirect(url_for('client.client_contact_list'))



@client.get('/soassales/client/scouting-list')
def scout_list():
	url = baseURL+''.join('scouts')
	scoutlist = requests.get(url)
	
	if scoutlist.status_code == 200:
		det = scoutlist.json()
	else:
		det = None


	cl = countries()
	countrylist = cl.split(',')

	return render_template('client/scout_list.html', cl=countrylist, det=det, menu=menu, submenu='sl')


@client.get('/soassales/client/scouting/add-record')
def add_scout():
	cl = countries()
	countrylist = cl.split(',')
	return render_template('client/add_scout.html', cl=countrylist, menu=menu, submenu='sl')


@client.post('/soassales/client/scouting/save-record')
def save_add_scout():
	if request.method == 'POST':
		current_user = 1
		try:
			data = {
				"name": request.form['name'],
				"email": request.form['email'],
				"industry": request.form['industry'],
				"country": request.form['country'],
				"address": request.form.get('address'),
				"createdby": current_user
			}

			url = baseURL+''.join('scouts/add')
			save = requests.post(url, json=data)

			if save.status_code == 200:
				det = save.json()
				flash("Record created", "primary")
			else:
				det = save.json()
				flash(det['msg'], "danger")

		except Exception as e:
			flash(e, "danger")
	
	return redirect(url_for('client.add_scout'))


@client.post('/soassales/client/scouting/update-record')
def update_scout():
	if request.method == 'POST':
		current_user = 1
		try:
			data = {
				"id": request.form['id'],
				"name": request.form['name'],
				"email": request.form['email'],
				"industry": request.form['industry'],
				"country": request.form['country'],
				"address": request.form.get('address'),
				"comment": request.form.get('comment'),
				"status": request.form['status']
			}

			url = baseURL+''.join('scouts/update')
			save = requests.patch(url, json=data)

			if save.status_code == 200:
				det = save.json()
				flash("Record Updated", "primary")
			else:
				det = save.json()
				flash(det['msg'], "danger")

		except Exception as e:
			flash(e, "danger")
	return redirect(url_for('client.scout_list'))


@client.delete('/soassales/client/scouting/delete-record')
def delete_scout():
	return redirect(url_for('client.scout_list'))




@client.add_app_template_filter
def get_contact(clientid):
	url = baseURL+''.join(f'clients/contact/list/{clientid}')
	clientlist = requests.get(url)
		
	if clientlist.status_code == 200:
		det = clientlist.json()
	else:
		det = None

	return det

