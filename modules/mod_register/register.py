from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy

from modules.models import *

register = Blueprint('register', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(register)

@register.route('/register', methods=['GET', 'POST'])
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
                        role=Role.customer.value
                    )

                    db.session.add(new_user)
                    db.session.commit()

                    add_customer_account(username, Role.customer.value)

                except sqlalchemy.exc.IntegrityError:
                    return redirect(url_for('register.show') + '?error=user-or-email-exists')

                return redirect(url_for('login.show') + '?success=account-created')
        else:
            return redirect(url_for('register.show') + '?error=missing-fields')
    else:
        return render_template('register.html')


def add_customer_account(username, role):
    user = Users.query.filter_by(username=username).first()
    if user:
        if role == Role.customer.value:
            new_account = Customer(
                C_Id=user.id,
                C_De=0,
                C_Cre=0,
                C_Bal=0,
            )
            db.session.add(new_account)
            db.session.commit()
        elif role == Role.admin.value or role == Role.operator.value:
            new_account = Staff(
                S_Id=user.id,
                S_Post="hello?",
                S_Status=Status.free.value
            )
            db.session.add(new_account)
            db.session.commit()