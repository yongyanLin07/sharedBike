import os

from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash

from modules.models import db, Users, Role, Bikes

bikeReport = Blueprint('bikeReport', __name__, template_folder='../templates')

basedir = os.path.abspath(os.path.dirname(__file__))


@bikeReport.route('/bikeReport', methods=['post'])
def bikeReport():
    img = request.files.get('txt_photo')
    username = request.form.get("name")
    path = basedir + "/static/photo/"
    file_path = path + img.filename
    img.save(file_path)
    print
    '上传头像成功，上传的用户是：' + username
    return render_template('index.html')

# @bikeReport.route('/bikeReport', methods=['GET', 'POST'])
# def show():
#     if request.method == 'POST':
#         bikeSelect = request.form['id']
#         # print(bikeSelect)
#
#         if bikeSelect:
#             if bikeSelect is not None:
#                 bike = Bikes.query.filter(Bikes.B_Id == bikeSelect).one()
#                 if bike.B_Status == 2:
#                     print(bike.B_Id)
#                     bike.B_Status = 1
#                     db.session.commit()
#                     print("success")
#                 else:
#                     redirect(url_for('bikeRent.show') + '?error=can-not-open')
#     return render_template('bikeRent.html')