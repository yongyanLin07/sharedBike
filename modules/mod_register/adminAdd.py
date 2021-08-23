from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import sqlalchemy

from modules.models import db, Users, Role


adminAdd = Blueprint('adminAdd', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(adminAdd)

@adminAdd.route('/adminAdd', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if username and email and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(
                    password, method='sha256')
                try:
                    new_user = Users(
                        username=username,
                        email=email,
                        password=hashed_password,
                        role=Role.admin.value
                    )

                    db.session.add(new_user)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    return redirect(url_for('adminAdd.show') + '?error=user-or-email-exists')
        return render_template('showUser.html')
    else:
        return render_template('adminAdd.html')

    #
    #     else:
    #         return redirect(url_for('adminAdd.show') + '?error=missing-fields')
    # else:
    #     return render_template('adminAdd.html')
