import os.path
import datetime
from flask import request, render_template, session
from sales import create_app
from urllib.parse import urlparse


app = create_app()


if __name__ == '__main__': 
	app.run(debug=True, port=8000)



@app.before_request
def before_request():
    session.permanent = True
    create_app.permanent_session_lifetime = datetime.timedelta(minutes=15)
    session.modified = True



@app.errorhandler(404)
def page_not_found(e):
    last_url = request.base_url
    path_domain = getPath(last_url)

    return render_template('404.html', error_msg=e, path=path_domain)


@app.errorhandler(500)
def internal_server_error(e):
    last_url = request.base_url
    path_domain = getPath(last_url)
    return render_template('server_error.html', error_msg=e, path=path_domain)


@app.errorhandler(405)
def method_not_allowed(e):
    last_url = request.base_url
    path_domain = getPath(last_url)
    return render_template('server_error.html', error_msg=e, path=path_domain)


def getPath(last_url):
    path = urlparse(last_url).path
    sections = []; temp="";

    while path != '/':
        temp = os.path.split(path)
        path =  temp[0]
        sections.append(temp[1])
    
    path_domain = ''
    
    return path_domain