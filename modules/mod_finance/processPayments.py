from flask import Blueprint, render_template, url_for, redirect, flash, session
from flask_login import current_user, login_required
import stripe

from modules.models import db, rentingRecord, Customer

processPayments = Blueprint('processPayments', __name__, template_folder='../templates')
loc_name = None
bikeSelect = None

STRIPE_PUBLIC_KEY="pk_test_51ILtOcK7WvdteM7JBGpZsCIfOxPk2Zsj7jMk7mG15Pe7yWnX0p5DDF991WqdAChyKhQhX8XCYihcgTRaA8nz1g3d006Edg7xYK"
STRIPE_SECRET_KEY="sk_test_51ILtOcK7WvdteM7J1wW3Qpyu5pFAAckaGntHPQqhVvunJnShY63cdsahkAQSWA56xmmJ158dgIEjxAazIzOWVmMD00ORMeWLso"

stripe_keys = {
  'secret_key': STRIPE_SECRET_KEY,
  'publishable_key': STRIPE_PUBLIC_KEY
}

stripe.api_key = stripe_keys['secret_key']

@processPayments.route('/payment', methods=['GET', 'POST'])
@login_required
def payment_page():
    if 'rent_record_id' in session:
        record_id = session['rent_record_id']
        unpaid_record = rentingRecord.query.filter(rentingRecord.R_Id == record_id, rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).one()
    else:
        unpaid_record = rentingRecord.query.filter(rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).first()
    
    fare = unpaid_record.R_fee
    
    return render_template('payment.html', key=stripe_keys['publishable_key'], fare=fare)

@processPayments.route('/processPaymentByCard', methods=['GET', 'POST'])
@login_required
def payment_by_card():
    
    if 'rent_record_id' in session:
        record_id = session['rent_record_id']
        unpaid_record = rentingRecord.query.filter(rentingRecord.R_Id == record_id, rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).one()
    else:
        unpaid_record = rentingRecord.query.filter(rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).first()
    
    if unpaid_record is not None:
        unpaid_record.R_Paid = 1
        
        db.session.commit()
        
    return render_template('paymentComplete.html')

@processPayments.route('/processPaymentByWallet', methods=['GET', 'POST'])
@login_required
def payment_by_wallet():
    if 'rent_record_id' in session:
        record_id = session['rent_record_id']
        print("in session ",record_id)
        unpaid_record = rentingRecord.query.filter(rentingRecord.R_Id == record_id, rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).one()
    else:
        unpaid_record = rentingRecord.query.filter(rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).first()
    
    customer = Customer.query.filter_by(C_Id = current_user.id).first()
    if customer is not None:
        if(float(customer.C_Bal) >= float(unpaid_record.R_fee)):
            customer.C_Bal -= unpaid_record.R_fee
            customer.C_Bal = round(customer.C_Bal, 1)
            db.session.commit()
        else:
            flash("Insufficient balance in wallet")
            return redirect(url_for('processPayments.payment_page') + '?error=insufficient-balance')
    
    if unpaid_record is not None:
        unpaid_record.R_Paid = 1
        
        db.session.commit()
    return render_template('paymentComplete.html')