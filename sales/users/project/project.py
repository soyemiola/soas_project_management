from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
import requests
from sales import baseURL
from datetime import datetime, timedelta
from flask_login import current_user



project = Blueprint('project', __name__, url_prefix='/', template_folder='templates')

menu = 'project'

@project.before_request
def chk_session():
    if not current_user.is_authenticated:
        return redirect(url_for('user.auth_login', next=request.url))


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
				"createdby": current_user.id,
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
				"createdby": current_user.id,
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
	try:
		# get project details
		project_url = baseURL+''.join(f'projects/details/{id}')
		project = requests.get(project_url)
		uproject = project.json()


		if project.status_code != 200:
			# put request response in nested if condition
			flash(clist['msg'], 'danger')
		else:
			# project contact user
			client_id = uproject['data']['client_id']
			contact_ids = uproject['data']['contact_ids']

			project_client_contacts_url = baseURL+''.join(f'contacts/project/{client_id}/contacts/{contact_ids}')
			project_contacts = requests.get(project_client_contacts_url)
			uproject_contacts = project_contacts.json()


			# project team members
			team_lead_id = uproject['data']['team_lead_id']
			team_ids = uproject['data']['team_ids']

			project_team_members_url = baseURL+''.join(f'contacts/project/team/{team_lead_id}/members/{team_ids}')
			project_team = requests.get(project_team_members_url)
			uproject_team = project_team.json()

			details = {
				"contacts": uproject_contacts,
				"team_members": uproject_team
			}


			# project items
			item_url = baseURL+''.join(f'projects/item/{id}/get-item')
			items = requests.get(item_url)
			uitems = items.json()


	except:
		uproject, details, uitems = None, None, None

		flash('Error fetching record', 'danger')
		return redirect(url_for('project.project_list'))

	return render_template('project/project_details.html', project=uproject, details=details, uitems=uitems, menu=menu, submenu='pr')


@project.post('/soassales/project/add-item')
def project_add_item():
	if request.method == 'POST':
		project_id = request.form['project_id']
		try:
			data = {
				"userid": current_user.id,
				"project_id": project_id,
				"subject": request.form['subject'],
				"description": request.form['description'],
				"note": request.form.get('note'),
				"postdate": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
				"actionables_id": request.form.getlist('actionables_id'),
				"actionables_task": request.form.getlist('actionables_task'),
				"deliverables": request.form.getlist('deliverables')
			}

			add_item_url = baseURL+''.join('projects/item/project')
			save_item = requests.post(add_item_url, json=data)

			det = save_item.json()

			if save_item.status_code != 200:
				flash(det['msg'], 'danger')
			else:
				flash("New item added", "primary")

		except Exception as e:
			flash(e, 'danger')

		return redirect(url_for('project.project_details', id=project_id))


@project.post('/soassales/project/update-item')
def project_update_item():
	if request.method == 'POST':
		project_id = request.form['project_id']
		try:
			data = {
				"userid": current_user.id,
				"project_id": project_id,
				"subject": request.form['subject'],
				"description": request.form['description'],
				"note": request.form.get('note'),
				"postdate": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
				"actionables_id": request.form.getlist('actionables_id'),
				"actionables_task": request.form.getlist('actionables_task'),
				"deliverables": request.form.getlist('deliverables')
			}

			add_item_url = baseURL+''.join('projects/item/project')
			save_item = requests.post(add_item_url, json=data)

			det = save_item.json()

			if save_item.status_code != 200:
				flash(det['msg'], 'danger')
			else:
				flash("New item added", "primary")

		except Exception as e:
			flash(e, 'danger')

		return redirect(url_for('project.project_details', id=project_id))


@project.post('/soassales/project/project-item/<int:project_id>/comment')
def project_item_comment(project_id):
	if request.method == 'POST':
		try:
			date = datetime.today()

			data = {
				"project_item_id": request.form['project_item_id'],
				"userid": current_user.id,
				"comment": request.form['comment'],
				"postdate": date.strftime('%Y-%m-%dT%H:%M:%S')
			}

			comment_url = baseURL+''.join('comments/project/project-item/comment')
			save_comment = requests.post(comment_url, json=data)

			det = save_comment.json()

			if save_comment.status_code != 200:
				flash(det['msg'], 'danger')
			else:
				flash('Comment added', 'primary')
				
			return redirect(url_for('project.project_details', id=project_id))

		except Exception as e:
			flash(e, 'danger')
			return redirect(url_for('project.project_details', id=project_id))


@project.get('/soassales/project/user/actionable')
def project_actionable():
	
	actionable_url = baseURL+''.join(f'actionable/project-list/{current_user.id}')
	res = requests.get(actionable_url)
	det = res.json()

	if res.status_code != 200:
		flash(det['msg'], 'danger')
		det = None

	return render_template('project/project_actionable.html', det=det, menu=menu, submenu='ac')


@project.get('/soassales/project/user/project/<int:taskid>/actionable/<int:project_item_id>/details')
def project_actionable_info(taskid, project_item_id):
	
	# all pending task list
	pending_url = baseURL+''.join(f'actionable/project-task/incomplete/{current_user.id}/{taskid}')
	pending_res = requests.get(pending_url)
	pending_list_det = pending_res.json()

	# current task info
	task_url = baseURL+''.join(f'actionable/project-task/{project_item_id}/details/{taskid}')
	task_res = requests.get(task_url)
	task_list_det = task_res.json()

	if pending_res.status_code != 200:
		pending_list_det = None

	if task_res.status_code != 200:
		task_list_det = None

	pr = taskid, project_item_id

	return render_template('project/project_actionable_info.html', task_det=task_list_det, pend_list=pending_list_det,
							pr=pr, menu=menu, submenu='ac')



@project.post('/soassales/project/<taskid>/<project_item_id>/task/feedback')
def task_feedback(taskid, project_item_id):
	if request.method == 'POST':
		
		try:
			data = {
				"project_item_id": request.form['project_item_id'],
				"task_id": request.form['actionable_id'],
				"userid": current_user.id,
				"feedback": request.form['feedback'],
				"postdate": datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			}

			feedback_url = baseURL+''.join(f'actionable/project-task/add-feedback')
			res = requests.post(feedback_url, json=data)
			response = res.json()

			if res.status_code != 200:
				flash(response['msg'], 'danger')
			else:
				flash('Feedback added', 'primary')

		except Exception as e:
			flash(e, 'danger')
			
		return redirect(url_for('project.project_actionable_info', taskid=taskid, project_item_id=project_item_id))
	else:
		return redirect(url_for('project.project_actionable_info', taskid=taskid, project_item_id=project_item_id))


@project.post('/soassales/project/<taskid>/<project_item_id>/task/update')
def task_status_update(taskid, project_item_id):
	if request.method == 'POST':
		
		try:
			data = {
				"project_item_id": request.form['project_item_id'],
				"actionables_id": request.form['actionable_id'],
				"userid": current_user.id,
				"status": request.form['status'],
				"comment": request.form.get('comment'),
				"postdate": datetime.today().strftime("%Y-%m-%d %H:%M:%S")
			}

			status_url = baseURL+''.join(f'actionable/project-task/status/update')
			res = requests.patch(status_url, json=data)
			response = res.json()

			if res.status_code != 200:
				flash(response['msg'], 'danger')
			else:
				flash('Record updated', 'primary')

		except Exception as e:
			flash(e, 'danger')
			
		return redirect(url_for('project.project_actionable_info', taskid=taskid, project_item_id=project_item_id))
	else:
		return redirect(url_for('project.project_actionable_info', taskid=taskid, project_item_id=project_item_id))



@project.add_app_template_filter
def convert_date_time(date):
	new = datetime.today().strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
	return new


@project.add_app_template_filter
def convert_date(date):
	try:
		new = datetime.today().strptime(date, "%Y-%m-%dT%H:%M:%S")
		_date = new.strftime("%Y-%m-%d")
		_time = new.strftime("%H:%M:%S")

		return _date, _time
	except:
		return None


@project.add_app_template_filter
def last_comment_time(date):
	current_time = datetime.now()
	time = datetime.today().strptime(date, '%Y-%m-%dT%H:%M:%S')
	
	time_diff = current_time - time
	
	time_in_seconds = int(time_diff.total_seconds())

	return format_time(duration=time_in_seconds)


@project.add_app_template_filter
def last_comment_time2(date):
	current_time = datetime.now()
	time = datetime.today().strptime(date, '%Y-%m-%d %H:%M:%S')
	
	time_diff = current_time - time
	
	time_in_seconds = int(time_diff.total_seconds())

	return format_time(duration=time_in_seconds)



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
		url = baseURL+''.join(f'contacts/project/{client_id}/contacts/{contact_list}')
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
		return None


@project.add_app_template_filter
def project_comment_list(project_item_id):
	try:
		url = baseURL+''.join(f'comments/project-item/{project_item_id}/comment-list')
		det = requests.get(url)
		return det.json()
	except Exception as e:
		return None


@project.add_app_template_filter
def user_comment_img(project_item_id):
	try:
		url = baseURL+''.join(f'comments/project-item/{project_item_id}/comment-users')
		det = requests.get(url)
		return det.json()
	except Exception as e:
		return None


@project.add_app_template_filter
def count_actionable_comment(actionable_id):
	try:
		url = baseURL+''.join(f'actionable/project-task/comment-count/{actionable_id}')
		det = requests.get(url)
		return det.json()
	except Exception as e:
		return None



def format_time(duration):
	minutes, seconds = divmod(duration, 60)
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)

	if days > 0:
		return f'{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)'
	elif hours > 0:
		return f'{hours} hour(s), {minutes} minute(s), {seconds} second(s)'
	elif minutes > 0:
		return f'{minutes} minute(s), {seconds} second(s)'
	else:
		return f'{seconds} second(s)'