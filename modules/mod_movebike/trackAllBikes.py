from flask import Blueprint, render_template
from flask_login import login_required
from modules.models import Bikes

trackAllBikes = Blueprint('trackAllBikes', __name__, template_folder='../templates')


@trackAllBikes.route('/trackAllBikes', methods=['GET', 'POST'])
@login_required
def show_all_bikes():
            
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

    return render_template('trackAllBikes.html', bikes_dict=bikes_dict)