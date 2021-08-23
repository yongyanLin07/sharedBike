from flask import Blueprint, url_for, render_template, redirect, request, flash
from modules.models import movingRecord, Bikes, db ,Staff, Locations
moveAdd = Blueprint('moveAdd', __name__, template_folder='../templates')


@moveAdd.route('/moveAdd', methods=['GET', 'POST'])
def add():
    locations = Locations.query.all()
    bikes = Bikes.query.all()
    bikes_dict = {}

    status = {1:"In Use", 2:"Available", 3:"Under Repair", 4:"In Transit"}

    for b in bikes:
        B_Status_String = status[b.B_Status]
        if b.B_Current not in bikes_dict:
            bikes_dict[b.B_Current] = [[b.B_Id, B_Status_String, b.B_Price]]
        else:
            old_val = bikes_dict[b.B_Current]
            old_val.append([b.B_Id, B_Status_String, b.B_Price])
            bikes_dict[b.B_Current] = old_val

    for k,v in bikes_dict.items():
        print(f'{k}')
        print(f'len {len(v)}')
        for value in v:
            print(f'Bike Id {value[0]} Status {value[1]} Price {value[2]}')

    operators = Staff.query.all()
    operators_dict = {}

    status1 = {'1': "free", '2': "busy"}

    for o in operators:
        O_Status_String = status1[o.S_Status]
        if o.S_Post not in operators_dict:
            operators_dict[o.S_Post] = [[o.S_Id, O_Status_String]]
        else:
            old_val = operators_dict[o.S_Post]
            old_val.append([o.S_Id, O_Status_String])
            operators_dict[o.S_Post] = old_val

    for k,v in operators_dict.items():
        print(f'{k}')
        print(f'len {len(v)}')
        for value in v:
            print(f'Operator Id {value[0]} Status {value[1]} ')
    if request.method == 'POST':
        error = None
        b_id = request.form['b_id']
        s_id = request.form['s_id']
        position = request.form['position'] # get the destination of this movement action
        status = 'open'
        if b_id and s_id and position:
            # check the bike's status to ensure if it can be moved
            current_bike = Bikes.query.get(b_id)
            if current_bike is not None:
                if current_bike.B_Status != 2:
                    error = "bike is not available to move now"
                    return render_template('moveAdd.html', error=error, locations=locations,bikes_dict=bikes_dict,operators_dict=operators_dict)

            else:
                error = "bike doesn't exist"
                return render_template('moveAdd.html', error=error, locations=locations,bikes_dict=bikes_dict,operators_dict=operators_dict)

            current_staff = Staff.query.get(s_id)
            # check the staff's status to ensure if he can do this work
            if current_staff is not None:
                if current_staff.S_Status == '2':
                    error = "this staff is busy now"
                    return render_template('moveAdd.html', error=error, locations=locations,bikes_dict=bikes_dict,operators_dict=operators_dict)
                else:
                    # set bike status to move
                    current_bike.B_Status = 4
                    db.session.commit()
                    new_mb_record = movingRecord(
                        B_Id=b_id,
                        S_Id=s_id,
                        MB_Post=position,
                        MB_Status=status
                    )
                    db.session.add(new_mb_record)
                    db.session.commit()
                    flash('Transfer request has been successfully registered.')
                    return redirect(url_for('moveAdd.add'))
            else:
                error = "staff doesn't exist"
                return render_template('moveAdd.html', error=error, locations=locations,bikes_dict=bikes_dict,operators_dict=operators_dict)
    else:
        #get the information of all the bikes
        return render_template('moveAdd.html',locations=locations, bikes_dict=bikes_dict,operators_dict=operators_dict)