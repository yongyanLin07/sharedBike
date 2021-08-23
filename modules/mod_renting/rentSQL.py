from flask import Blueprint, url_for, render_template, redirect, request, jsonify
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import sqlalchemy

from modules.models import db, Users, Role, rentingRecord
rentSQL = Blueprint('rentSQL', __name__, template_folder='../frontend')

@rentSQL.route('/rentSQL')
def show_page():
    userTable = rentingRecord.query.all()
    return render_template('rentSQL.html', article=userTable)

