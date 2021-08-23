from flask import Blueprint, url_for, render_template, redirect, request, session
from flask_login import current_user

from modules.models import movingRecord, Staff, db

staffMovingBike = Blueprint('staffMovingBike', __name__, template_folder='../templates')


@staffMovingBike.route('/staffMovingBike', methods=['GET', 'POST'])
def show():
    if request.method == 'GET':
        # get current staff id
        s_id = current_user.get_id();
        lists = movingRecord.query.filter(movingRecord.S_Id == s_id).all()
        return render_template('bikeMove.html', lists=lists)
    else:
        error = None
        s_id = current_user.get_id();
        order_id = request.form['order_id']
        staff = Staff.query.get(s_id)
        # check the staff current status to ensure he can start the task
        if staff.S_Status == '2':
            error = 'You are not available now'
            lists = movingRecord.query.filter(movingRecord.S_Id == s_id).all()
            return render_template('bikeMove.html', lists=lists, error=error)
        # get the movement task
        order = movingRecord.query.get(order_id)
        # set the order's status running
        order.MB_Status = 'running'
        db.session.commit()

        # set the staff's status busy
        staff.S_Status = '2'
        db.session.commit()

        lists = movingRecord.query.filter(movingRecord.S_Id == s_id).all()
        return render_template('bikeMove.html', lists=lists)
