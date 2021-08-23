from datetime import datetime
from flask import Blueprint, url_for, redirect, request, flash
from flask_login import current_user

from modules.models import movingRecord, Staff, db, Bikes

staffFinishMoving = Blueprint('staffFinishMoving', __name__, template_folder='../templates')


@staffFinishMoving.route('/staffFinishMoving', methods=['POST'])
def finish():
    if request.method == 'POST':

        order_id = request.form['order_id']
        # get current order
        current_order = movingRecord.query.get(order_id)
        s_id = current_user.get_id()
        # get staff
        staff = Staff.query.get(s_id)
        # update staff status
        staff.S_Post = current_order.MB_Post
        staff.S_Status = '1'
        db.session.commit()
        # update bike status
        current_bike = Bikes.query.get(current_order.B_Id)
        current_bike.B_Current = current_order.MB_Post
        current_bike.B_Status = '2'
        db.session.commit()
        # close this movement task
        current_order.MB_Status = 'close'
        # save end time
        close_date = datetime.utcnow()
        current_order.MB_CloseTime = close_date
        db.session.commit()
        flash('You have finished this task')
        return redirect(url_for('staffMovingBike.show'))