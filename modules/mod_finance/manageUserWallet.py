from flask import Blueprint, render_template, flash, request
from flask_login import current_user, login_required
import stripe
from modules.models import db, Customer

manageUserWallet = Blueprint('manageUserWallet', __name__, template_folder='../templates')
loc_name = None
bikeSelect = None

STRIPE_PUBLIC_KEY="pk_test_51ILtOcK7WvdteM7JBGpZsCIfOxPk2Zsj7jMk7mG15Pe7yWnX0p5DDF991WqdAChyKhQhX8XCYihcgTRaA8nz1g3d006Edg7xYK"
STRIPE_SECRET_KEY="sk_test_51ILtOcK7WvdteM7J1wW3Qpyu5pFAAckaGntHPQqhVvunJnShY63cdsahkAQSWA56xmmJ158dgIEjxAazIzOWVmMD00ORMeWLso"

stripe_keys = {
  'secret_key': STRIPE_SECRET_KEY,
  'publishable_key': STRIPE_PUBLIC_KEY
}

stripe.api_key = stripe_keys['secret_key']

@manageUserWallet.route('/walletInfo', methods=['GET', 'POST'])
@login_required
def wallet_info():
    
    customer = Customer.query.filter_by(C_Id = current_user.id).first()
    balance = round(customer.C_Bal, 1)
    print(balance)
    if(request.method=='POST'):
        try:
            recharge_amount = request.form['recharge_amount']
            
            balance += float(recharge_amount)
            
            customer.C_Bal = balance
            
            db.session.commit()
            flash("Money successfully added to the wallet!")
        except:
            flash("There was an error adding money to your wallet, Please try again later!")
            return render_template('walletInfo.html', key=stripe_keys['publishable_key'], balance=balance)
        
    return render_template('walletInfo.html', key=stripe_keys['publishable_key'], balance=balance)