from flask import Blueprint, render_template, request, redirect, url_for
from modules.models import db, Maintenance, Staff, MaintenanceRecord, Customer
from flask_login import login_required

staffDistribution = Blueprint('staffDistribution', __name__, template_folder='../templates')


@staffDistribution.route('/staffDistribution')
@login_required
def show():
    m_id=request.args.get('reportId')
    openreport = Maintenance.query.filter(Maintenance.M_Id == m_id)
    
    operators = Staff.query.filter(Staff.S_Status=='1').all()
    operators_dict = {}
    
    for o in operators:
        if o.S_Post not in operators_dict:
            operators_dict[o.S_Post] = [[o.S_Id]]
        else:
            old_val = operators_dict[o.S_Post]
            old_val.append([o.S_Id])
            operators_dict[o.S_Post] = old_val
    
    return render_template('staffDistribution.html', article=openreport, operators=operators_dict)


@staffDistribution.route('/arrange', methods=['post','get'])
@login_required
def arrange():
    if request.method == 'get':
        print("enter get")
        pass
    else:
        s_id = request.form['id']
        print(s_id)
        if s_id:
            try:
                m_id = request.args.get('id')
                staff = Staff.query.filter(Staff.S_Id == s_id).one()
                print(staff.S_Status)
                if staff.S_Status == '1':
                    print(m_id)
                    new_m_arrange = MaintenanceRecord(
                        S_Id=staff.S_Id,
                        M_Id=m_id,
                        MR_Result='open'
                    )
                    db.session.add(new_m_arrange)
                    report = Maintenance.query.filter(Maintenance.M_Id == m_id).one()
                    report.M_Status = 'Distribution'
                    staff.S_Status = '2'
                    
                    customer = Customer.query.filter(Customer.C_Id == report.C_Id).one()
                    customer.C_Bal += 0.5
                    
                    db.session.commit()
                    print('You have reported successfully')
                    return redirect(url_for('home.show'))
                else:
                    return redirect(url_for('staffDistribution.show') + '?error=staff-not-available&reportId='+str(m_id))
            except:
                return redirect(url_for('staffDistribution.show') + '?error=staff-not-available&reportId='+str(m_id))
        # except Exception as e:
        #     return redirect(url_for('staffDistribution.show') + '?error=can-not-open')
    # else:
    #     return render_template('staffDistribution.html')
    
@staffDistribution.route('/displayUserImage',methods=['POST'])
@login_required
def display_user_image():
    if request.method=='POST':
        m_id = request.args.get('id')
        print(m_id)
        report = Maintenance.query.filter(Maintenance.M_Id == m_id).one()
        filename = report.M_ImagePath.split('/')[3]
        print(filename)
        return redirect(url_for('static', filename='customer_images/'+filename))