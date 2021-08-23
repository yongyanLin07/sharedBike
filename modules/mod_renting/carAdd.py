from flask import Blueprint, url_for, render_template, redirect, request
# from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import sqlalchemy

from modules.models import db, Bikes

carAdd = Blueprint('carAdd', __name__, template_folder='../templates')


@carAdd.route('/carAdd', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        id = request.form['id']
        service_date = request.form['service_date']
        health_status = request.form['health_status']
        return redirect(url_for('carAdd.show') + '?error=missing-fields')
        # print(id)

        if id and service_date and health_status:
            new_car = Bikes(
                id=id,
                service_date=service_date,
                health_status=health_status
            )
            db.session.add(new_car)
            # print("add successful")
            db.session.commit()
            # print("commit successful")
        else:
            return redirect(url_for('carAdd.show') + '?error=missing-fields')
    else:
        return render_template('carAdd.html')