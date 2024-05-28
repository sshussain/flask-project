from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

user_admin = Blueprint('user_admin', __name__, template_folder='templates')


@user_admin.route('/login')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)
