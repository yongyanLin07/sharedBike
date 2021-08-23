from flask import Blueprint, request, render_template, flash
from modules.models import db, Locations
from sqlalchemy import func
from flask_login import login_required
addNewLocation = Blueprint('addNewLocation', __name__)

@addNewLocation.route('/addNewLocation',methods=['GET','POST'])
@login_required
def showReport():
    
    if request.method == 'POST':
        loc_name = request.form['loc_name']
        
        if loc_name is not None and str(loc_name).replace(' ', '').isalpha():
            loc_name = str(loc_name).title()
            loc_exists = Locations.query.filter(func.lower(Locations.Loc_Name)==func.lower(loc_name)).first()
            print(loc_name)
            print(loc_exists)
            if loc_exists is None:
                location = Locations(Loc_Name=loc_name)
                db.session.add(location)
                db.session.commit()
                flash(f"{loc_name} added in Locations!")
            else:
                flash(f"{loc_name} already exits!")
        else:
            flash("Please enter a valid location")
            
    return render_template('addNewLocation.html')
    
