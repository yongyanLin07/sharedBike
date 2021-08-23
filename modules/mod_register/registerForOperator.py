from flask import Blueprint, url_for, render_template, redirect, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import sqlalchemy

from modules.models import db, Users, Role, Staff, Status, Customer, Locations
import random

registerForOperator = Blueprint('registerForOperator', __name__, template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(registerForOperator)

@registerForOperator.route('/registerForOperator', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        role = int(request.form.get('role'))
        print(role)

        if username and email and password and confirm_password and role:
            if password == confirm_password:
                hashed_password = generate_password_hash(
                    password, method='sha256')
                try:
                    new_user = Users(
                        username=username,
                        email=email,
                        password=hashed_password,
                        role=role
                    )

                    db.session.add(new_user)
                    db.session.commit()

                    add_customer_account(username, role)
                except sqlalchemy.exc.IntegrityError:
                    return redirect(url_for('registerForOperator.show') + '?error=user-or-email-exists')

                return redirect(url_for('registerForOperator.show') + '?success=account-created')
        else:
            return redirect(url_for('registerForOperator.show') + '?error=missing-fields')
    else:
        return render_template('registerForOperator.html')


def add_customer_account(username, role):
    print("enter operator success")
    user = Users.query.filter_by(username=username).first()
    print(user)
    if user:
        print(role)
        print(Role.customer.value)
        print(Role.operator.value)
        if role == Role.customer.value:
            new_account = Customer(
                C_Id=user.id,
                C_De=0,
                C_Cre=0,
                C_Bal=0,
            )
            db.session.add(new_account)
            db.session.commit()
            print("ok")
            
        end_loc = Locations.query.all()
        end_locs = []
        for loc in end_loc:
            end_locs.append(loc.Loc_Name)
        end_loc = random.choice(end_locs)
        
        if role == Role.operator.value:
            new_account = Staff(
                S_Id=user.id,
                S_Post=end_loc,
                S_Status=Status.free.value
            )
            print("operator success")
            db.session.add(new_account)
            db.session.commit()