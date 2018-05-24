import datetime

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, current_user, logout_user
import config
from exts import *
from models import *
from exts import db, login_manager, load_user
import json
import random
import time

"""
本文件内主要包含各个地址的路由
"""

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
login_manager.init_app(app)

# 生成mac随机地址
def randomMAC():
    mac = [random.randint(0x00, 0x7f),
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))

# 购买探针地址的路由
@app.route("/buy", methods=["GET"])
def buy():
    username = request.args.get("username")
    return render_template("pricing_tables.html", username=username)

# 主页面的路由
@app.route('/', methods=["GET"])
@login_required
def index():
    username = current_user.username
    return render_template("index.html", username=username)

# wifi表格的路由
@app.route('/table_wifi', methods=["GET"])
@login_required
def table_wifi():
    username = current_user.username
    return render_template("table_wifi.html", username=username)

# mac表格的路由 这里是随机生成的表格
@app.route('/table_mac', methods=["GET"])
@login_required
def table_mac():
    username = current_user.username
    mac_table = []
    for i in range(10):
        li = {"mac": randomMAC(),
              "online": "是" if random.random() >= 0.5 else "否",
              "last_time": datetime.datetime(2017, 11, 24 + random.randint(0, 3)).strftime("%Y-%m-%d"),
              "early_time": datetime.datetime(2017, 11, 22 + random.randint(0, 1)).strftime("%Y-%m-%d"),
              "hold_time": str(random.randint(30, 59)) + "分钟",
              "times": random.randint(5, 10)
              }
        mac_table.append(li)
    return render_template("table_mac.html", username=username, mac_table=mac_table)

# 获取日期的数据
@app.route("/date", methods=["GET"])
@login_required
def date():
    username = current_user.username
    return render_template("date.html", username=username)

# 添加wifi探针的路由
@app.route("/add_wifi", methods=["GET"])
@login_required
def add_wifi():
    username = current_user.username
    return render_template("add_wifi.html", username=username)

# 获取数据的路由
@app.route("/data/<info>")
@login_required
def data(info):
    my_id = current_user.id
    wifi_ids = []  # 用户绑定的wifi id号
    user_wifis = UserWithWifi.query.filter(UserWithWifi.userId == my_id).all()
    for user_wifi in user_wifis:
        wifi_ids.append(user_wifi.wifiId)
    data = []
    if info == 'user_number':
        user_numbers = UserNumber.query.filter(UserNumber.id == wifi_ids[0]).order_by(UserNumber.time).all()
        for user_number in user_numbers:
            data.append([int(user_number.time.timestamp() * 1000), user_number.number])
    elif info == 'user_rate':
        user_rates = UserRate.query.filter(UserRate.id == wifi_ids[0]).order_by(UserRate.time).all()
        for user_rate in user_rates:
            data.append([int(user_rate.time.timestamp() * 1000), user_rate.rate])
    elif info == 'stay_time':
        stay_times = Stay.query.filter(Stay.id == wifi_ids[0]).order_by(Stay.time).all()
        for stay_time in stay_times:
            data.append([int(stay_time.time.timestamp() * 1000), stay_time.stay])
    elif info == "periodic":
        periodics = Periodic.query.filter(Periodic.id == wifi_ids[0]).order_by(Periodic.time).all()
        for periodic in periodics:
            data.append([int(periodic.time.timestamp() * 1000), periodic.space])
    return json.dumps(data)

# 登录的路由
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        number = request.form.get("number")
        password = request.form.get("password")
        filter_user = User.query.filter(User.number == number).first()
        if filter_user is None:
            flash("没有此用户")
        else:
            if not filter_user.verify_password(password):
                flash("密码不正确")
            else:
                login_user(filter_user)
                return redirect(url_for("index"))
        return redirect(url_for("login"))

# 注销的路由
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

# 注册的路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return redirect("login#signup")
    else:
        username = request.form.get("username")
        number = request.form.get("number")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if username is "" or number is "" or "" is None or "" is None:
            flash("请输入有效值")
        elif password1 != password2:
            flash("两次输入密码结果不一致")
        else:
            filter_user = User.query.filter(User.number == number).first()
            if filter_user:
                flash("已经存在这个账号，请换一个账号")
            else:
                user = User()
                user.number = number
                user.username = username
                user.set_password(password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login"))
        return redirect(url_for("login") + "#signup")

# 绑定探针的路由
@app.route("/bind", methods=["GET"])
@login_required
def bind():
    username = current_user.username
    return render_template("bind.html", username=username)


# 绑定结果的路由
@app.route("/bind_data", methods=["POST"])
def bind_data():
    wifi_id = request.form.get("wifi_id")
    wifi_pin_filter = wifiPin.query.filter(wifiPin.id == wifi_id).first()
    if wifi_pin_filter is None:
        return render_template("bind_data.html", message="探针不存在")
    else:
        if UserWithWifi.query.filter(UserWithWifi.wifiId == wifi_id).first() is None:
            db.session.add(UserWithWifi(current_user.id, wifi_id))
            db.session.commit()
            return render_template("bind_data.html", message="成功绑定")
        else:
            return render_template("bind_data.html", message="该探针已被绑定，请联系管理员")

# 500 错误的路由
@app.errorhandler(500)
def internal_error(url):
    return render_template("page_500.html"), 500

# 404 错误的路由
@app.errorhandler(404)
def not_found(url):
    """
    url: /hello
    result: not found: 'hello'
    """
    return render_template("page_404.html"), 404

# 程序启动
if __name__ == '__main__':
    app.run(debug=True, port=8889)
