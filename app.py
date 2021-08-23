from flask import Flask
import os
from flask_login import LoginManager

from modules.models import db, Users, Bikes

from modules.index import index
from modules.mod_register.login import login
from modules.mod_register.logout import logout
from modules.mod_register.register import register
from modules.home import home
# from carAdd import carAdd
# from showUser import showUser
from modules.mod_register.adminAdd import adminAdd
# from showUserSQL import showUserSQL, deleteSQL
from werkzeug.security import generate_password_hash

from modules.mod_register.showUserSQL import showUserSQL
from modules.mod_register.registerForOperator import registerForOperator
from modules.mod_register.changePassword import changePassword

from modules.mod_renting.bikeRent import bikeRent
from modules.mod_renting.bikeSQL import bikeSQL
from modules.mod_renting.rentSQL import rentSQL

# repairing bike
from modules.mod_repair.reporterror import reporterror
from modules.mod_repair.distribution import distribution, approveSQL
from modules.mod_repair.staffDistribution import staffDistribution
from modules.mod_repair.finish import finishSQL

# moving bike
from modules.mod_movebike.moveAdd import moveAdd
from modules.mod_movebike.staffMovingBike import staffMovingBike
from modules.mod_movebike.finishMoving import staffFinishMoving
from modules.mod_movebike.operatorDashBoard import operatorDashBoard
#manager data reports
from modules.mod_viewreports.viewDataReports import viewDataReports
from modules.mod_register.addNewLocation import addNewLocation
from modules.mod_register.addNewBike import addNewBike
from modules.mod_movebike.trackAllBikes import trackAllBikes
# finance
from modules.mod_finance.processPayments import processPayments
from modules.mod_finance.manageUserWallet import manageUserWallet

app = Flask(__name__)
secret_key = os.urandom(16)

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database/database.db'
app.config['DEBUG'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
login_manager = LoginManager()
login_manager.init_app(app)

# register and login edited by tianyi
db.init_app(app)
app.app_context().push()
app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(home)
app.register_blueprint(adminAdd)
app.register_blueprint(showUserSQL)
# app.register_blueprint(deleteSQL)
app.register_blueprint(registerForOperator)
app.register_blueprint(changePassword)

# renting bike edited by tianyi
db.init_app(app)
app.app_context().push()
# app.register_blueprint(carAdd)
app.register_blueprint(bikeRent)
app.register_blueprint(bikeSQL)
app.register_blueprint(rentSQL)

# repairing bike edited by yuqi
app.register_blueprint(reporterror)
app.register_blueprint(distribution)
app.register_blueprint(approveSQL)
app.register_blueprint(staffDistribution)
app.register_blueprint(finishSQL)

# moving bike by yongyan
app.register_blueprint(moveAdd)
app.register_blueprint(staffMovingBike)
app.register_blueprint(staffFinishMoving)
app.register_blueprint(operatorDashBoard)

#manager data reports
app.register_blueprint(viewDataReports)

# finance
app.register_blueprint(processPayments)
app.register_blueprint(manageUserWallet)

app.register_blueprint(addNewLocation)
app.register_blueprint(addNewBike)
app.register_blueprint(trackAllBikes)
db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


def create_admin():
    admin_exists = Users.query.filter_by(username='admin').first()
    if admin_exists is None:
        new_user = Users(
            username='admin',
            email='admin',
            password= generate_password_hash( 'admin', method='sha256'),
            role=2
        )

        db.session.add(new_user)
        db.session.commit()


def add_bike():
    bike = Bikes(
        B_Price=1,
        B_Status=2,
        B_Current='West End'
    )
    db.session.add(bike)
    db.session.commit()


if __name__ == '__main__':
    create_admin()
    # add_bike()
    app.run(host='127.0.0.1', port=8000)
