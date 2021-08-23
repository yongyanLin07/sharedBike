from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from enum import Enum, unique

db = SQLAlchemy()


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String)
    role = db.Column(db.Integer)


class Bikes(db.Model):
    B_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    B_Price = db.Column(db.String(32))
    B_Status = db.Column(db.Integer)
    B_Current = db.Column(db.String(64))


class Customer(UserMixin, db.Model):
    C_Id = db.Column(db.Integer, primary_key=True)
    # C_Username = db.Column(db.String, unique=True)
    # C_Mail = db.Column(db.String(50), unique=True)
    # C_Pw = db.Column(db.String(50))
    C_De = db.Column(db.Integer)  ## Debit
    C_Cre = db.Column(db.Integer)  ## Credit
    C_Bal = db.Column(db.Integer)  ## Balance(De-Ce)


class Staff(UserMixin, db.Model):
    S_Id = db.Column(db.Integer, primary_key=True)
    # S_Username = db.Column(db.String, unique=True)
    S_Post = db.Column(db.String(50))
    # S_Mail = db.Column(db.String(50), unique=True)
    # S_Pw = db.Column(db.String(50))
    S_Status = db.Column(db.String(50))  # 1,2,3 free busy break
    # S_Role = db.Column(db.Integer) # 1 for op 2 for admin


class rentingRecord(db.Model):
    R_Id = db.Column(db.Integer, primary_key=True)
    C_Id = db.Column(db.Integer)
    B_Id = db.Column(db.Integer)
    R_St = db.Column(db.DateTime)  # START TIME
    R_Et = db.Column(db.DateTime)  # END TIME
    R_Sp = db.Column(db.String(50))  # START POSITION
    R_Ep = db.Column(db.String(50))  # END POSITION
    R_fee = db.Column(db.Integer)
    R_Paid = db.Column(db.String(50))


class Maintenance(db.Model):
    M_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    C_Id = db.Column(db.Integer)
    B_Id = db.Column(db.Integer)
    M_Error = db.Column(db.String(50))
    M_Time = db.Column(db.DateTime)  # Report time
    M_Status = db.Column(db.String(50))  # close open Distribution
    M_ImagePath = db.Column(db.String(150))


class MaintenanceRecord(db.Model):
    MR_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    S_Id = db.Column(db.Integer)
    M_Id = db.Column(db.Integer)
    MR_Time = db.Column(db.DateTime)  # Finished time
    MR_Result = db.Column(db.String(50))  # finish open


class movingRecord(db.Model):
    MB_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    B_Id = db.Column(db.Integer)
    S_Id = db.Column(db.Integer)
    MB_Post = db.Column(db.String(50))
    MB_StartTime = db.Column(db.DATETIME, default=datetime.now)
    MB_CloseTime = db.Column(db.DATETIME)
    MB_Status = db.Column(db.String(50))# open / close
    
class Locations(db.Model):
    L_Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Loc_Name = db.Column(db.String(100))


@unique
class Role(Enum):
    customer = 1
    admin = 2
    operator = 3


class Status(Enum):
    free = 1
    busy = 2
    # break


@unique
class bikeStatus(Enum):
    use = 1
    available = 2
    repair = 3
    move = 4


@unique
class paidStatus(Enum):
    paid = 1
    unpaid = 2
