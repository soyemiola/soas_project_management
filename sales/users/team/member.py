from flask import Blueprint, render_template, redirect, url_for


member = Blueprint('member', __name__, url_prefix='/', template_folder='templates')

menu = 'team'

@member.get('/soassales/v1/member-list')
def member_list():
	return render_template('members/member-list.html', menu=menu, submenu="ml")


@member.get('/soassales/v1/member-list/new-record')
def member_new_record():
	return render_template('members/member_new_record.html', menu=menu, submenu="ml")


@member.post('/soassales/v1/member-list/new-record')
def member_new_record_save():
	if request.method == 'POST':
		pass
	return redirect(url_for('member.member_list'))


@member.get('/soassales/v1/member/<int:id>/member-edit')
def member_edit(id):
	return render_template('members/member_edit.html', menu=menu, submenu="ml")



@member.patch('/soassales/v1/member-update')
def member_update(id):
	return redirect(url_for('member.member_list'))



@member.delete('/soassales/v1/member/member-delete')
def member_delete():
	if request.method == 'DELETE':
		userid = request.form['user_id']
		flash('Record Deleted', 'success')
	else:
		flash('Invalid method', 'danger')
	
	return redirect(url_for('member.member_list'))



@member.get('/soassales/v1/member/member-role-list')
def member_role_list():
	return render_template('members/member_role_list.html', menu=menu, submenu="mr")


@member.get('/soassales/v1/member/member-role-add')
def add_member_role():
	return render_template('members/add_member_role.html', menu=menu, submenu="mr")


@member.post('/soassales/v1/member-role-save')
def save_member_role():
	return redirect(url_for('member.member_role_list'))


@member.get('/soassales/v1/member/<int:id>/member-role-update')
def edit_member_role(id):
	return render_template('members/edit_member_role.html', menu=menu, submenu="mr")


@member.delete('/soassales/v1/member/member-delete')
def member_role_delete():
	if request.method == 'DELETE':
		userid = request.form['role_id']
		flash('Record Deleted', 'success')
	else:
		flash('Invalid method', 'danger')
	
	return redirect(url_for('member.member_list'))