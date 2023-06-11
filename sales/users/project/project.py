from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
import requests
from sales import baseURL

project = Blueprint('project', __name__, url_prefix='/', template_folder='templates')

menu = 'project' 


@project.get('/soassales/project-list')
def project_list():
	try:
		url = baseURL+''.join('projects')

		project = requests.get(url)

		projectList = project.json()

		if project.status_code != 200:
			flash(clist['msg'], 'danger')
	except:
		clist=None
		flash('Error connecting to API server', 'danger')

	project_status = ['Ongoing', 'Completed', 'Pending', 'Terminated']
	return render_template('project/project_list.html', status=project_status, projects=projectList, menu=menu, submenu='pr')


@project.get('/soassales/project/project-new')
def new_project():
	try:
		url = baseURL+''.join('clients')
		user_url = baseURL+''.join('users')

		clients = requests.get(url)
		users = requests.get(user_url)

		clist = clients.json()
		ulist = users.json()

		if clients.status_code != 200 or users.status_code != 200:
			flash(clist['msg'], 'danger')
	except:
		clist=None
		flash('Error connecting to API server', 'danger')

	return render_template('project/new_project.html', clist=clist, ulist=ulist, menu=menu, submenu='pr')


@project.post('/soassales/project/project-save-record')
def save_new_project():
	if request.method == 'POST':
		try:
			current_user = 1
			data = {
				"name": request.form['project_name'],
				"description": request.form['project_desc'],
				"ptype": request.form['project_type'],
				"location": request.form.get('project_address'),
				"date": request.form['project_date'],
				"client_id": request.form['project_client_id'],
				"contact_ids": request.form.getlist('project_contact_ids'),
				"team_lead_id": request.form['project_team_lead'],
				"team_ids": request.form.getlist('project_team'),
				"createdby": current_user,
				"comment": request.form.get('project_comment')
			}

			url = baseURL+''.join('projects/new-project')
			save = requests.post(url, json=data)

			res = save.json()

			if save.status_code != 200:
				flash(res['msg'], 'danger')
			else:
				flash('Project created', 'primary')

			return redirect(url_for('project.new_project'))
		except Exception as e:
			flash(e, 'danger')
			return redirect(url_for('project.new_project'))


@project.get('/soassales/project/<int:id>/edit-project-record')
def edit_project(id): 
	try:
		# get clients
		url = baseURL+''.join('clients')
		clients = requests.get(url)
		
		# get users
		user_url = baseURL+''.join('users')
		users = requests.get(user_url)

		# get project details
		project_url = baseURL+''.join(f'projects/one/{id}')
		project = requests.get(project_url)

		
		clist = clients.json()
		ulist = users.json()
		uproject = project.json()
		
		client_id = uproject['data']['client_id']

		# get project client contacts list
		client_contact_url = baseURL+''.join(f'contacts/client/{client_id}')
		client_contact = requests.get(client_contact_url)

		ucontact_user = client_contact.json()


		if clients.status_code != 200 or users.status_code != 200 or project.status_code != 200:
			# put request response in nested if condition
			flash(clist['msg'], 'danger')
	except:
		clist, ulist, uproject, ucontact_user = None, None, None, None
		flash('Error connecting to API server', 'danger')
	return render_template('project/edit_project.html', project=uproject, clist=clist, ccu=ucontact_user, ulist=ulist, menu=menu, submenu='pr')


@project.post('/soassales/project/project-save-record')
def update_project():
	if request.method == 'POST':
		try:
			current_user = 1
			data = {
				"project_id": request.form['project_id'],
				"name": request.form['project_name'],
				"description": request.form['project_desc'],
				"ptype": request.form['project_type'],
				"location": request.form.get('project_address'),
				"date": request.form['project_date'],
				"client_id": request.form['project_client_id'],
				"contact_ids": request.form.getlist('project_contact_ids'),
				"team_lead_id": request.form['project_team_lead'],
				"team_ids": request.form.getlist('project_team'),
				"createdby": current_user,
				"comment": request.form.get('project_comment')
			}

			url = baseURL+''.join('projects/update')
			update = requests.patch(url, json=data)

			res = update.json()

			if update.status_code != 200:
				flash(res['msg'], 'danger')
			else:
				flash('Project created', 'primary')

			return redirect(url_for('project.project_list'))
		except Exception as e:
			flash(e, 'danger')
			return redirect(url_for('project.project_list'))



@project.delete('/soassales/project/project-record-delete')
def delete_project():
	return redirect(url_for('project.project_list'))


@project.get('/soassales/project/<int:id>/project-progress-details')
def project_details(id):
	return render_template('project/project_details.html', menu=menu, submenu='pr')


@project.get('/soassales/project/user/actionable')
def project_actionable():
	return render_template('project/project_actionable.html', menu=menu, submenu='ac')


@project.get('/soassales/project/user/project/<int:id>/actionable/details')
def project_actionable_info(id):
	return render_template('project/project_actionable_info.html', menu=menu, submenu='ac')



@project.add_app_template_filter
def get_client_info(client_id):
	url = baseURL+''.join(f'clients/one/{client_id}')
	client = requests.get(url)
	if client.status_code == 200:
		record = client.json()
		return record
	else:
		return None

@project.add_app_template_filter
def get_client_project_contacts(client_id, contact_list):
	try:
		url = baseURL+''.join(f'contacts/client/{client_id}/project/contacts/{contact_list}')
		details = requests.get(url)
		return details.json()
	except:
		return None

@project.add_app_template_filter
def get_project_team_details(team_lead_id, team_ids):
	try:
		url = baseURL+''.join(f'users/project/team/{team_lead_id}/team-members/{team_ids}')
		det = requests.get(url)
		return det.json()
	except Exception as e:
		# enter log value
		return None