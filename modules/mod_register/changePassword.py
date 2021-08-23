from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy

from modules.models import db, Users, Role

changePassword = Blueprint('changePassword', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(changePassword)


@changePassword.route('/changePassword', methods=['GET', 'POST'])
def change():
    if request.method == 'POST':

        old_password = request.form.get('old-password')
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        id = request.args.get('id')

        if old_password and password and confirm_password and id:
            user = Users.query.filter(Users.id == id).one()
            print(user.password)
            if user is not None and password == confirm_password:
                user.password = generate_password_hash(
                    password, method='sha256')
                db.session.commit()
                print("success")
                # if not check_password_hash(user.password, old_password):
                #     return redirect(url_for('changePassword.change') + '?error=wrong-password')
                # ####todo COMMIT NEW PASSWORD
                # try:
                #
                #     hashed_password = generate_password_hash(
                #         password, method='sha256')
                #     user.password = hashed_password
                #
                #     db.session.commit(user)
                #     print("success")
                # except Exception as e:
                #     return redirect(url_for('changePassword.change') + '?error=%s'.format(e))

                return redirect(url_for('home.show'))
        else:
            return redirect(url_for('changePassword.change') + '?error=missing-fields')
    else:
        return render_template('changePassword.html')
