from flask import Blueprint, url_for, render_template, redirect, request, jsonify
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import sqlalchemy

from modules.models import db, Users, Role,Staff
showUserSQL = Blueprint('showUserSQL', __name__, template_folder='../../template')
deleteSQL = Blueprint('deleteSQL', __name__, template_folder='../../template')


# @showUserSQL.route('/showUserSQL')
# def show_page():
#     userTable = Users.query.all()
#     return render_template('showUserSQL.html', article=userTable)


@showUserSQL.route('/showUserSQL')
def show_page():
    userTable = Staff.query.all()
    return render_template('showUserSQL.html', article=userTable)


@deleteSQL.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        Need_id = int(request.args.get('id'))
        print(Need_id)
    ## to do: how to get id from front???
        # js = request.get_json()
        # Need_id = request.form['username']
        # 查询数据库是否有对应id的需求
        Delete = Users.query.get(Need_id)
        if Delete:
            try:
                db.session.delete(Delete)
                db.session.commit()
                # return jsonify({"code": "0000", "msg": "success"})
                userTable = Users.query.all()
                return render_template('showUserSQL.html', article=userTable)
            except Exception as e:
                db.session.rollback()
        else:
            return jsonify({"code": "0000", "msg": "failed"})
