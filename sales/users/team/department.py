from flask import Blueprint, render_template, redirect, url_for


department = Blueprint('department', __name__, url_prefix='/', template_folder='templates')

menu = 'department'


@department.get('/soassales/v1/department-list')
def department_list():
	return render_template('department/department_list.html', menu=menu, submenu="dpt")



@department.get('/soassales/v1/department/add-new-record')
def add_department():
	return render_template('department/add_department.html', menu=menu, submenu="dpt")


@department.post('/soassales/v1/department/department-save-record')
def save_add_department():
	return redirect(url_for('department.department_list'))


@department.get('/soassales/v1/department/<int:id>/department-edit')
def edit_department(id):
	return render_template('department/edit_department.html', menu=menu, submenu="dpt")


@department.delete('/soassales/v1/department/department-delete')
def delete_department():
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