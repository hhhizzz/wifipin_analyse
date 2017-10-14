from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, current_user
import config
from exts import User
from exts import db, login_manager, load_user

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
login_manager.init_app(app)


@app.route("/buy", methods=["GET"])
def buy():
    username = request.args.get("username")
    return render_template("pricing_tables.html", username=username)


@app.route('/', methods=["GET"])
@login_required
def index():
    username = current_user.username
    return render_template("index.html", username=username)


@app.route('/index2', methods=["GET"])
@login_required
def index2():
    username = current_user.username
    return render_template("index2.html", username=username)


@app.route("/date", methods=["GET"])
@login_required
def date():
    username = current_user.username
    return render_template("date.html", username=username)


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


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    return "logout page"


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


@app.errorhandler(500)
def internal_error(url):
    return render_template("page_500.html"), 500


@app.errorhandler(404)
def not_found(url):
    """
    url: /hello
    result: not found: 'hello'
    """
    return render_template("page_404.html"), 404


if __name__ == '__main__':
    app.run(debug=True, port=8888)
