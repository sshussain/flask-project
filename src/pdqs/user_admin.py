from flask import Blueprint, render_template, request

user_admin = Blueprint('user_admin', __name__, template_folder='templates')


@user_admin.route('/', methods=['GET'])
def landing():
    # Show sign-in page
    return render_template(f"pages/login.html")


@user_admin.route('/login', methods=['POST'])
def login_user():
    # Extract name and password from the form
    uname = request.form['uname']
    upwd = request.form['upwd']
    if not uname and not upwd:
        return render_template(f'pages/create.html')
    # Send a new cookie


# TODO. Send sign-up page
@user_admin.route('/create', methods=['POST'])
def create_user():
    ...
