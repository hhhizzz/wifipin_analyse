import os

DEBUG = True

SECRET_KEY = os.urandom(24)
extend_existing = True

HOSTNAME = 'localhost'
PORT = "3306"
DATABASE = 'wifiPin'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
