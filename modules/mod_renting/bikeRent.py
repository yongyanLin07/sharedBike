from flask import Blueprint, url_for, render_template, redirect, request, session, flash
from flask_login import current_user, login_required
from datetime import datetime

from modules.models import db, Bikes, rentingRecord, Locations

import random

bikeRent = Blueprint('bikeRent', __name__, template_folder='../templates')
loc_name = None
bikeSelect = None

@bikeRent.route('/showBikes', methods=['GET', 'POST'])
@login_required
def show_bikes():
    global loc_name
    
    try:
        
        unpaid_record = rentingRecord.query.filter(rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).first()
        if unpaid_record:
            session['rent_record_id'] = unpaid_record.R_Id
            
            if(unpaid_record.R_Ep is None):
                return render_template('tripStarted.html', start_location=unpaid_record.R_Sp)
            else:
                distance = round(random.uniform(0.1,10.0),1)
                time_diff = unpaid_record.R_Et - unpaid_record.R_St
                time = str(time_diff).split('.')[0]
                return render_template('tripEnded.html', start_location=unpaid_record.R_Sp, end_location=unpaid_record.R_Ep, distance=distance, fare=unpaid_record.R_fee, time=time)
    except Exception as e:
        print("No record")
        print(e)
    
    locations = Locations.query.all()
    if request.method == 'POST':
        loc_name = request.form['loc_name']
        
        bikes = Bikes.query.filter(Bikes.B_Current == loc_name, Bikes.B_Status == 2).all()
        bikes_count = Bikes.query.filter(Bikes.B_Current == loc_name, Bikes.B_Status == 2).count()
        
        distances = [round((random.random()+0.1),1) for i in range(len(bikes))]
        distances = sorted(distances)
        if(bikes_count<=0):
            flash(f"No bikes available at {loc_name}")
        return render_template('showBikes.html', locations=locations, bikes=bikes, distances=distances, selected_loc=loc_name)
            
    return render_template('showBikes.html', locations=locations)

@bikeRent.route('/bikeRent', methods=['GET', 'POST'])
def rent_bike():
    if request.method == 'POST':
        global bikeSelect
        bikeSelect = request.form['bike_id']
        print(bikeSelect)
        if bikeSelect:
            if bikeSelect is not None:
                bike = Bikes.query.filter(Bikes.B_Id == bikeSelect).one()
                # print(bike.B_Status)
                # #test
                # bike.B_Status = 1
                # db.session.commit()
                # print("success")
                # todo: modift the databse(finish)
                if bike.B_Status == 2:
                    # change bike status
                    bike.B_Status = 1
                    db.session.commit()
                    # add record to renting dataset start
                    add_renting_record(bike)
                    unpaid_record = rentingRecord.query.filter(rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).one()
                    session['rent_record_id'] = unpaid_record.R_Id
                else:
                    pass
                    # redirect(url_for('showBikes.show') + '?error=can-not-open')
    return render_template('tripStarted.html', start_location=loc_name)


@bikeRent.route('/closeBike', methods=['GET', 'POST'])
def close():
    if request.method == 'POST':
        # todo: find the record in the user that have not lock the bike to get the bike ID
        # rentRecord = rentingRecord.query.all()
        if 'rent_record_id' in session:
            record_id = session['rent_record_id']
            unpaid_record = rentingRecord.query.filter(rentingRecord.R_Id == record_id, rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).one()
        else:
            unpaid_record = rentingRecord.query.filter(rentingRecord.C_Id == current_user.id, rentingRecord.R_Paid == 2).first()
        # add_close_record(unpaid_record)
        bikeSelect = unpaid_record.B_Id
        loc_name = unpaid_record.R_Sp
        
        end_loc = Locations.query.filter(Locations.Loc_Name != loc_name).all()
        end_locs = []
        for loc in end_loc:
            end_locs.append(loc.Loc_Name)
        end_loc = random.choice(end_locs)
        
        distance = round(random.uniform(0.1,10.0),1)
        
        time_diff = datetime.utcnow() - unpaid_record.R_St
        hours = time_diff.total_seconds() / 3600
        time = str(time_diff).split('.')[0]
        print(time)
        print(hours)
        
        fare = 0.5
        
        print(bikeSelect)
        if bikeSelect:
            if bikeSelect is not None:
        
                bike = Bikes.query.filter(Bikes.B_Id == bikeSelect).one()
                if(hours>1):
                    fare = round(float(bike.B_Price) * hours, 1)
                else:
                    fare = bike.B_Price
                    
                if bike.B_Status == 1:
                    # change bike status
                    bike.B_Status = 2
                    bike.B_Current = end_loc
                    db.session.commit()
                    # add record to renting dataset start
                    add_close_record(unpaid_record, end_loc, fare)
                else:
                    redirect(url_for('bikeRent.show') + '?error=can-not-open')
    return render_template('tripEnded.html', start_location=loc_name, end_location=end_loc, distance=distance, fare=fare, time=time)


def add_renting_record(bike):
    # todo:using token to know who the use is (finished)
    # user = Users.query.filter_by(username=username).first()
    rent = rentingRecord(
        C_Id=current_user.id,
        B_Id=bike.B_Id,
        R_St=datetime.utcnow(),
        R_Sp=loc_name,
        R_Paid=2,
    )
    print(rent)
    db.session.add(rent)
    db.session.commit()


def add_close_record(unpaid_record, end_loc, fare):
    # todo:using token to know who the use is (finished)
    # user = Users.query.filter_by(username=username).first()
    
    unpaid_record.R_Et=datetime.utcnow()
    unpaid_record.R_Ep=end_loc
    unpaid_record.R_fee=fare
    unpaid_record.R_Paid = 2
    db.session.commit()


