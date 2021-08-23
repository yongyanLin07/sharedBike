from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from modules.models import db, Bikes, Locations

addNewBike = Blueprint('addNewBike', __name__, template_folder='../templates')


@addNewBike.route('/addNewBike', methods=['GET', 'POST'])
@login_required
def add_bike():
    locations = Locations.query.all()
    if request.method == 'POST':
        loc_name = request.form['loc_name']
        price = request.form['price']
        status = request.form['status']
    
        # return redirect(url_for('carAdd.show') + '?error=missing-fields')

        if ( loc_name and price and status) is not None:
            new_bike = Bikes(
                B_Price=price,
                B_Status=status,
                B_Current = loc_name
            )
            db.session.add(new_bike)
            db.session.commit()
            
            flash("Bike added successfully!")    
        else:
            print(f"Invalid data {price} {status} {loc_name}")

    return render_template('addNewBike.html', locations=locations)