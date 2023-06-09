from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from sales import baseURL
import requests



member = Blueprint('member', __name__, url_prefix='/', template_folder='templates')

menu = 'team'

@member.get('/soassales/member-list')
def member_list():
	try:
		url = baseURL+''.join('users') 
		scoutlist = requests.get(url)
		
		if scoutlist.status_code == 200:
			det = scoutlist.json()
		else:
			det = None
	except Exception as e:
		flash(e, 'danger')

	return render_template('members/member-list.html', users=det, menu=menu, submenu="ml")


@member.get('/soassales/member-list/new-record')
def member_new_record():
	try:
		url = baseURL+''.join('users/roles')
		roles = requests.get(url)
		if roles.status_code == 200:
			det = roles.json()
		else:
			det = None
		
	except Exception as e:
		flash('Error fetching record', "danger")
  
	return render_template('members/member_new_record.html', roles=det, menu=menu, submenu="ml")


@member.post('/soassales/member-list/new-record')
def member_new_record_save():
	if request.method == 'POST':
		current_userid = 1
		try:
			data = {
				"fullname": request.form['fullname'],
				"organization": request.form['organization'],
				"department": request.form['department'],
				"email": request.form['email'],
				"number": request.form['number'],
				"role": request.form['role'],
				"createdby": current_userid
			}

			url = baseURL+''.join('users/new-record')
			new_record = requests.post(url, json=data)
			det = new_record.json()

			if new_record.status_code == 200:

				flash('New record created', 'primary')
				return redirect(url_for('member.member_list'))
			else:
				flash(det['msg'], 'info')
				return redirect(url_for('member.member_new_record'))

		except Exception as e:
			flash(e, 'danger')
			return redirect(url_for('member.member_new_record'))



@member.get('/soassales/member/<int:id>/member-edit')
def member_edit(id):
	url = baseURL+''.join(f'users/single/{ id }')
	res = requests.get(url)

	role_url = baseURL+''.join('users/roles')
	roles = requests.get(role_url)

	det = res.json()
	role_det = roles.json()

	if res.status_code == 200:
		det = res.json()
	else:
		flash(det['msg'], 'danger')
		return redirect(url_for('member.member_list'))

	return render_template('members/member_edit.html', user=det, roles=role_det, menu=menu, submenu="ml")



@member.post('/soassales/member-update')
def member_update():
	if request.method == 'POST':
		try:
			user_id = request.form['user_id']
			data = {
				"user_id": user_id,
				"fullname": request.form['fullname'],
				"organization": request.form['organization'],
				"department": request.form['department'],
				"email": request.form['email'],
				"number": request.form['number'],
				"role": request.form['role'],
				"status": request.form['status']
			}

			url = baseURL+''.join(f'users/update/{user_id}')
			update_record = requests.patch(url, json=data)
					
			det = update_record.json()
			
			if update_record.status_code == 200:

				flash(det['msg'], 'primary')
				
			else:

				flash(det['msg'], 'info')
			
			return redirect(url_for('member.member_edit', id=user_id))

		except Exception as e:
			flash(e, 'danger')
			return redirect(url_for('member.member_new_record'))
	return redirect(url_for('member.member_list'))



@member.post('/soassales/member/member-delete')
def member_delete():
	if request.method == 'POST':
		user_id = request.form['user_id']

		url = baseURL+''.join(f'users/delete/{ user_id }')
		res = requests.delete(url)
		
		det = res.json()

		if res.status_code == 200:
			flash(det['msg'], "primary")
		else:
			flash(det['msg'], 'danger')
	
	return redirect(url_for('member.member_list'))



@member.get('/soassales/member/member-role-list')
def member_role_list():
	try:
		url = baseURL+''.join('users/roles')
		roles = requests.get(url)

		if roles.status_code == 200:
			det = roles.json()

	except Exception as e:
		det = None
		flash("Error fetching record", "info")

	return render_template('members/member_role_list.html', roles=det, menu=menu, submenu="mr")


@member.get('/soassales/member/member-role-add')
def add_member_role():
	return render_template('members/add_member_role.html', menu=menu, submenu="mr")


@member.post('/soassales/member-role-save')
def save_member_role():
	if request.method == 'POST':
		user_id = 1
		try:
			data = {
				"role": request.form['role'],
				"createdby": user_id
			}

			url = baseURL+''.join('users/roles/new')
			res = requests.post(url, json=data)

			if res.status_code == 200:
				flash("New record created", "primary")
				return redirect(url_for("member.member_role_list"))
			else:
				flash('Error', "danger")
				return redirect(url_for("member.add_member_role"))

		except Exception as e:
			flash(e, "danger") 
			return redirect(url_for("member.add_member_role"))
	else:
		flash("Invalid Method", "danger")
		return redirect(url_for("member.member_role_list"))


@member.get('/soassales/member/<int:id>/member-role-update')
def edit_member_role(id):
	url = baseURL+''.join(f"users/roles/edit/{id}")
	
	res = requests.get(url)

	if res.status_code == 200:
		det = res.json()
	else:
		flash("Error fetching details", "danger")
		return redirect(url_for("member.member_role_list"))

	return render_template('members/edit_member_role.html', det=det, menu=menu, submenu="mr")

@member.post('/soassales/member/member-role-update')
def member_role_update():
	if request.method == 'POST':
		user_id = 1
		try:
			role_id = request.form['id']
			role = request.form['role']

			data = {
				"role_id": role_id,
				"role": role
			}

			url = baseURL+''.join("users/roles/update")
			res = requests.patch(url, json=data)

			if res.status_code == 200:
				det = res.json()

				flash(det['msg'], "primary")
				return redirect(url_for("member.member_role_list"))
			else:
				flash("Error updating record", "danger")
				return redirect(url_for("member.edit_member_role", id=role_id))

		except Exception as e:
			flash(e, "danger")
			return redirect(url_for("member.edit_member_role", id=role_id))


@member.post('/soassales/member/member-role-delete')
def member_role_delete():
	if request.method == 'POST':
		role_id = request.form['role_id']

		url = baseURL+''.join(f'users/roles/{ role_id }')
		res = requests.delete(url)
		det = res.json()

		if res.status_code == 200:
			flash(det['msg'], "primary")
		else:
			flash(det['msg'], 'danger')
	
	return redirect(url_for('member.member_role_list'))