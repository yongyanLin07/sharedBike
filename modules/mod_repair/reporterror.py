from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime
from modules.models import db, Maintenance, Bikes
from flask_login import current_user
import os
from werkzeug.utils import secure_filename
import random
import string

reporterror = Blueprint('reporterror', __name__, template_folder='../templates')
IMAGE_UPLOAD_PATH = './static/customer_images/'

@reporterror.route('/reporterror', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        b_id = request.form['bikeID']
        errors = request.form['errors']
        try:
            b_id = int(b_id)
            bike = Bikes.query.filter(Bikes.B_Id == b_id).one()
            new_m_report = Maintenance(
                C_Id=current_user.id,
                B_Id=bike.B_Id,
                M_Error=errors,
                M_Time=datetime.utcnow(),
                M_Status='open'
            )
            if 'image' in request.files:
                image = request.files['image']
                if not image.filename=='':
                    filename = secure_filename(image.filename)
                    ext = str(os.path.splitext(filename)[1])
                    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                    image_path = os.path.join(IMAGE_UPLOAD_PATH, name+ext)
                    print(image_path)
                    image.save(image_path)
                    
                    new_m_report.M_ImagePath = image_path
            
            db.session.add(new_m_report)
            db.session.commit()
            
            return redirect(url_for('home.show'))
        except Exception as e:
            print(e)
            return redirect(url_for('reporterror.add') + '?error=can-not-open')

    else:
        return render_template('reporterror.html')

