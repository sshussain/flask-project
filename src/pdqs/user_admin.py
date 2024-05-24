from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

user_admin = Blueprint('user_admin', __name__, template_folder='templates')