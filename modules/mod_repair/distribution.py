from flask import Blueprint, url_for, render_template, redirect, request, jsonify
from modules.models import db, Maintenance, Bikes, Customer
import json
distribution = Blueprint('distribution', __name__, template_folder='../templates')
approveSQL = Blueprint('approveSQL', __name__, template_folder='../templates')


@distribution.route('/distribution')
def show():
    openreport = Maintenance.query.filter_by(M_Status="open")
    return render_template('distribution.html', article=openreport)


@distribution.route('/close', methods=['POST'])
def close():
    if request.method == 'POST':
        m_id = int(request.args.get('id'))
        report = Maintenance.query.filter(Maintenance.M_Id == m_id).one()
        report.M_Status = 'close'
        db.session.commit()
        return redirect(url_for('distribution.show'))
    else:
        return render_template('distribution.html')


@approveSQL.route('/approve', methods=['post','get'])
def show():
    if request.method == 'get':
        m_id = int(request.args.get('id'))
        print(m_id)
        return redirect(url_for('distribution.show'))
    else:
        print("not post")
        m_id = int(request.args.get('id'))
        # print(m_id)
        # m_id = request.form['id']
        # m_id = int(request.args.get('id'))
        # print(m_id)
        report = Maintenance.query.filter(Maintenance.M_Id == m_id).one()
        bike = Bikes.query.filter(Bikes.B_Id == report.B_Id).one()
        # print(bike)
        bike.B_Status = 3
        db.session.commit()
        print("success")
        return redirect(url_for('staffDistribution.show', reportId=m_id))
        # return render_template('distribution.html')
        # print("enter")
#        data = request.get_data()
#       data = json.loads(data)
#         m_id = request.form['id']
    #     # m_id = int(request.args.get('id'))
    #     print(m_id)
    #     report = Maintenance.query.filter(Maintenance.M_Id == m_id).one()
    #     bike = Bikes.query.filter(Bikes.B_Id == report.B_Id).one()
    #     print(bike)
    #     bike.B_Status = 3
    #     db.session.commit()
    #     print("success")
    #     return redirect(url_for('staffDistribution.show'))
    # else:
    #     return render_template('distribution.html')







