from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from exts import db
"""
本文件主要包含用到的数据库表
"""

# 用户表 包含用户id密码相关信息，密码使用Flask内置的密码hash后存储
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

# Wi-Fi探针表 保存wifi探针信息
class wifiPin(db.Model):
    __tablename__ = "wifiPin"
    id = db.Column(db.String(10), primary_key=True)

# 用户使用Wi-Fi探针表
class UserWithWifi(db.Model):
    __tablename__ = "userWithWifi"
    userId = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    wifiId = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=False)

    def __init__(self, userid, wifiid):
        self.userId = userid
        self.wifiId = wifiid

# 用户数表
class UserNumber(db.Model):
    __tabblename__ = "UserNumber"
    id = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    number = db.Column(db.Integer, nullable=False, default=0)

# 用户停留数表
class UserRate(db.Model):
    __tabblename__ = "UserRate"
    id = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    rate = db.Column(db.Float, nullable=False, default=0.0)

# 用户停留时间表
class Stay(db.Model):
    __tabblename__ = "Stay"
    id = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    stay = db.Column(db.Float, nullable=False, default=0.0)

# 用户访问周期表
class Periodic(db.Model):
    __tabblename__ = "Periodic"
    id = db.Column(db.String(10), db.ForeignKey("wifiPin.id"), primary_key=True)
    time = db.Column(db.DateTime, primary_key=True)
    space = db.Column(db.Float, nullable=False, default=0.0)
