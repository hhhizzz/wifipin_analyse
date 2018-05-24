from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "login"
db = SQLAlchemy(use_native_unicode="utf8")

from models import User

# 用户登录的方法
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
