from flask import Blueprint, render_template, redirect, url_for, request


project = Blueprint('project', __name__, url_prefix='/', template_folder='templates')

menu = 'project' 


@project.get('/soassales/v1/project-list')
def project_list():
	return render_template('project/project_list.html', menu=menu, submenu='pr')


@project.get('/soassales/v1/project/project-new')
def new_project():
	return render_template('project/new_project.html', menu=menu, submenu='pr')


@project.post('/soassales/v1/project/project-save-record')
def save_new_project():
	return redirect(url_for('project.project_list'))


@project.get('/soassales/v1/project/<int:id>/edit-project-record')
def edit_project(id):
	return render_template('project/edit_project.html', menu=menu, submenu='pr')


@project.delete('/soassales/v1/project/project-record-delete')
def delete_project():
	return redirect(url_for('project.project_list'))


@project.get('/soassales/v1/project/<int:id>/project-progress-details')
def project_details(id):
	return render_template('project/project_details.html', menu=menu, submenu='pr')