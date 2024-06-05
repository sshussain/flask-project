from flask import Blueprint, render_template, request
import logging

user_admin = Blueprint('user_admin', __name__, template_folder='templates')


@user_admin.route('/', methods=['GET'])
def landing():
    # Show sign-in page
    return render_template(f"pages/login.html")


@user_admin.route('/login', methods=['POST'])
def login_user():
    # Extract name and password from the form
    logging.info(f"Login {request.form.items()}")
    for k, v in request.form.items():
        logging.info(f"key=<{k}, value={v}")
    return "login successful", 200
    # uname = request.form['uname']
    # upwd = request.form['upwd']
    # if not uname and not upwd:
    #     return render_template(f"pages/create.html")
    # Send a new cookie


# TODO. Send sign-up page
@user_admin.route('/create', methods=['POST'])
def create_user():
    ...

# if __name__ == '__main__':
#     d = {'1': 1, '2': 2}
#     for k,v in d.items():
#         print(type(k))
#         print(k)
