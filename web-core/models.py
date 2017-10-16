from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)


class wifiPin(db.Model):
    __tablename__ = "wifiPin"
    id = db.Column(db.String(10), primary_key=True)


class UserWithWifi(db.Model):
    __tablename__ = "userWithWifi"
    userId = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    wifiId = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=False)


class UserNumber(db.Model):
    __tabblename__ = "UserNumber"
    id = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=True)
    time = db.Column(db.Date, primary_key=True)
    number = db.Column(db.Integer, nullable=False, default=0)


class UserRate(db.Model):
    __tabblename__ = "UserRate"
    id = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=True)
    time = db.Column(db.Date, primary_key=True)
    rate = db.Column(db.Float, nullable=False, default=0.0)


class Stay(db.Model):
    __tabblename__ = "Stay"
    id = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=True)
    time = db.Column(db.Date, primary_key=True)
    stay = db.Column(db.Float, nullable=False, default=0.0)


class Periodic(db.Model):
    __tabblename__ = "Periodic"
    id = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=True)
    time = db.Column(db.Date, primary_key=True)
    space = db.Column(db.Float, nullable=False, default=0.0)
