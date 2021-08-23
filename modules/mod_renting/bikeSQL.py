from flask import Blueprint, url_for, render_template, redirect, request, jsonify
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import sqlalchemy

from modules.models import db, Users, Role,Bikes
bikeSQL = Blueprint('bikeSQL', __name__, template_folder='../template')



@bikeSQL.route('/bikeSQL')
def show_page():
    userTable = Bikes.query.all()
    return render_template('bikeSQL.html', article=userTable)


