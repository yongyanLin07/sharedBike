from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user

from modules.models import *
from flask_login import current_user
home = Blueprint('home', __name__)
login_manager = LoginManager()
login_manager.init_app(home)


# edited by tianyi
@home.route('/home', methods=['GET'])
@login_required
def show():
    if current_user.role == 1:
        customer = Customer.query.filter_by(C_Id = current_user.id).first()
        if current_user:
            return render_template('home.html', info = customer)
        else:
            return render_template('home.html?error_404')
    elif current_user.role == 2:
        # staff = Staff.query.filter_by(S_Id=current_user.id).first()
        if current_user:
            return render_template('home.html')
        else:
            return render_template('home.html?error_404')
    elif current_user.role == 3:
        staff = Staff.query.filter_by(S_Id=current_user.id).first()
        if current_user:
            return render_template('home.html', info=staff)
        else:
            return render_template('home.html?error_404')

