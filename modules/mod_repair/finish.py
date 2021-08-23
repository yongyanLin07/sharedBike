from flask import Blueprint, url_for, render_template, redirect, request
from datetime import datetime
from modules.models import db, Maintenance, Bikes, MaintenanceRecord, Staff
from flask_login import current_user
from sqlalchemy import and_
finishSQL = Blueprint('finishSQL', __name__, template_folder='../templates')


@finishSQL.route('/finish')
def show():
    try:
        now = MaintenanceRecord.query.filter(and_(MaintenanceRecord.S_Id == current_user.id, MaintenanceRecord.MR_Result == 'open')).one()
        openreport = Maintenance.query.filter(Maintenance.M_Id == now.M_Id)
    except Exception as e:
        return redirect(url_for('home.show') + '?no-task')
    return render_template('finish.html', article=openreport)


@finishSQL.route('/over', methods=['POST'])
def finish():
    if request.method == 'POST':
        m_id = int(request.args.get('id'))
        b_id = Maintenance.query.filter(Maintenance.M_Id == m_id).one()
        b_id.M_Status = "close"
        bike = Bikes.query.filter(Bikes.B_Id == b_id.B_Id).one()
        bike.B_Status = 2
        mr_time = MaintenanceRecord.query.filter(MaintenanceRecord.M_Id == m_id).one()
        mr_time.MR_Time = datetime.utcnow()
        mr_time.MR_Result = "finish"
        staffid=Staff.query.filter(Staff.S_Id == current_user.id).one()
        staffid.S_Status = '1'
        db.session.commit()
        return redirect(url_for('home.show'))
    else:
        return render_template('finish.html')