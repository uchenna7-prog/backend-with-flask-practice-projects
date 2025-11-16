from flask import Flask,jsonify,request,url_for,redirect,render_template,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, login_user, logout_user, current_user, UserMixin, login_required

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SECRET_KEY"] = "uchenna"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True,unique=True)
    username = db.Column(db.String(100),nullable=False)
    email_address = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)


    def __init__(self,username,email_address,password):
        self.username = username
        self.email_address = email_address
        self.password = generate_password_hash(password)

@app.route("/",methods=["POST","GET"])
def sign_Up():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        data = request.form
        new_username = data["name"]
        new_email_address = data["email"]

        new_password1 = data["password1"]
        new_password2 = data["password2"]

        if new_password1 != new_password2:
            flash("passwords don't match","danger")

        existing_user = User.query.filter_by(email_address=new_email_address).first()
        if existing_user:
            flash("Email already registered", "danger")
            return redirect(url_for("sign_Up"))

        new_user = User(username=new_username,email_address=new_email_address,password=new_password1)
        db.session.add(new_user)
        db.session.commit()

        flash("signed up successfully","success")

        return redirect(url_for("login"))

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        data = request.form
        username = data["name"]
        email_address = data["email"]
        password = data["password"]

        user = User.query.filter_by(email_address = email_address).first()
        if not user:
            flash("user account not found","danger")
            return redirect(url_for("login"))
        if not check_password_hash(user.password,password):
            flash("invalid password","danger")
            return redirect(url_for("login"))

        return redirect(url_for("sign-Up"))

@login_required
def dashboard():
    pass


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)