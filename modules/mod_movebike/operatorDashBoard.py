from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash
import sqlalchemy

from modules.models import db, Users, Role, Staff, Status, Customer

operatorDashBoard = Blueprint('operatorDashBoard', __name__, template_folder='../templates')


@operatorDashBoard.route('/operatorDashBoard', methods=['GET'])
def show():
    if request.method == 'GET':
        if current_user.role == 3:
            return render_template("operatorDashBoard.html")
        else:
            error = "You are not an operator"
            return render_template('operatorDashBoard.html', error=error)
