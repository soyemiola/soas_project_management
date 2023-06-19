from flask import Blueprint, render_template, redirect, url_for, request, flash, Response
from sales import baseURL
from flask_login import current_user
import requests

department = Blueprint('department', __name__, url_prefix='/', template_folder='templates')

menu = 'department'

@department.before_request
def chk_session():
    if not current_user.is_authenticated:
        return redirect(url_for('user.auth_login', next=request.url))


@department.get('/soassales/v1/department-list')
def department_list():
	try:
		url = baseURL+''.join('department') 
		deptlist = requests.get(url)
		
		if deptlist.status_code == 200:
			det = deptlist.json()
		else:
			det = None
	except Exception as e:
		det = None
		flash('Error in connection', 'danger')

	return render_template('department/department_list.html', dept=det, menu=menu, submenu="dpt")



@department.get('/soassales/v1/department/add-new-record')
def add_department():
	return render_template('department/add_department.html', menu=menu, submenu="dpt")


@department.post('/soassales/v1/department/department-save-record')
def save_add_department():
	if request.method == 'POST':
		
		try:
			data = {
				"name": request.form['name']
			}

			url = baseURL+''.join('department/add')
			new_record = requests.post(url, json=data)
			det = new_record.json()

			if new_record.status_code == 200:

				flash('New record created', 'primary')
				return redirect(url_for('department.department_list'))
			else:
				flash(det['msg'], 'info')
				return redirect(url_for('department.add_department'))

		except Exception as e:
			flash(e, 'danger')
			return redirect(url_for('department.add_department'))
	return redirect(url_for('department.add_department'))


@department.get('/soassales/v1/department/<int:id>/department-edit')
def edit_department(id):
	url = baseURL+''.join(f'department/one/{ id }')
	
	res = requests.get(url)

	if res.status_code == 200:
		det = res.json()
	else:
		flash(det['msg'], 'danger')
		return redirect(url_for('department.department_list'))

	return render_template('department/edit_department.html', dept=det, menu=menu, submenu="dpt")


@department.post('/soassales/department/update')
def update_department():
	if request.method == 'POST':
		try:
			
			data = {
				"id": request.form['id'],
				"name": request.form['name'],
				"old_name": request.form['old_name']
			}

			url = baseURL+''.join('department/update')
			update_record = requests.patch(url, json=data)
					
			det = update_record.json()
			
			if update_record.status_code == 200:

				flash(det['msg'], 'primary')
				
			else:

				flash(det['msg'], 'info')
			
			return redirect(url_for('department.department_list'))

		except Exception as e:
			flash(e, 'danger')
			return redirect(url_for('department.edit_department'))
	return redirect(url_for('department.edit_department'))




@department.delete('/soassales/v1/department/department-delete')
def delete_department():
	if request.method == 'POST':
		
		data = {
			"id": request.form['user_id']
		}

		url = baseURL+''.join('department/delete')
		res = requests.delete(url, json=data)
		
		det = res.json()

		if res.status_code == 200:
			flash(det['msg'], "primary")
		else:
			flash(det['msg'], 'danger')

	return redirect(url_for('department.department_list'))

#

@department.get('/soassales/v1/department/unit/unit-list')
def unit_list():
	return render_template('unit/unit_list.html', menu=menu, submenu="unt")


@department.get('/soassales/v1/department/unit/add-new-record')
def add_unit():
	return render_template('unit/add_unit.html', menu=menu, submenu="unt")


@department.post('/soassales/v1/department/unit/unit-save-record')
def save_add_unit():
	return redirect(url_for('department.unit_list'))


@department.get('/soassales/v1/department/unit/<int:id>/unit-edit')
def edit_unit(id):
	return render_template('unit/edit_unit.html', menu=menu, submenu="unt")


@department.delete('/soassales/v1/department/unit/unit-delete')
def delete_unit():
	return redirect(url_for('department.unit_list'))