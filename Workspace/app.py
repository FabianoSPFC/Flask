import sys
from flask import Flask, render_template, request, url_for, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(id):
    return User.get(id)

import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

class Form(Form):
    openid = StringField('openid', validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    senha = PasswordField("senha", validators=[DataRequired()])
    description = StringField("description", validators=[DataRequired()])
    value = StringField("value", validators=[DataRequired()])

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    value = db.Column(db.Integer,nullable=False)

    def __init__(self,name,description,value):
        self.name = name
        self.description = description
        self.value  = value
class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(38), nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

	def get_id(self):
		return unicode(self.id)

    def __init__(self,email,senha):
            self.email = email
            self.senha = senha

@app.route("/")
def index():
	return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Form()
    print("1")
    user = User.query.filter_by(email=form.email.data).first()
    print("2")
    print("4")
    if user and user.senha == form.senha.data:
        print("5")
        flash("Logged in")
        print("6")
        return redirect(url_for("index"))
    else:
        print("7")
        flash("Invalid login")
    print("5")
    return render_template("login.html",form=form)
    print("6")
    return "OK"

@app.route("/signup", methods=['GET', 'POST'])
def signup():

    form = Form()
    if request.method == 'POST':
        email = (request.form.get("email"))
        senha = (request.form.get("password"))
        new_user = User(email=email,senha=senha)


        db.session.add(new_user)
        db.session.commit()
        flash("User Successfully Registered")
    return render_template("signup.html")

if __name__ == "__main__":
	app.run(debug=True)
