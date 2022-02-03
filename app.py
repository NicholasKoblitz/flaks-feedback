from flask import Flask, render_template, redirect, session
from models import db, connect_db, User
from forms import CreateUserForm


app = Flask(__name__)
app.config["SECRET_KEY"] +"quiinnfhyeteenhcllskjf7199275364l"
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///flask-feedback'
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

connect_db(app)

# ---------- Page Routes ---------------

@app.route("/")
def redirect_to_register():
    """Directs user to register form"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def get_register_form():
    """Gets register form"""

    form = CreateUserForm()

    if form.validate_on_submit():
        
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username

        return redirect("/secret")
    else:
        return render_template("register.html", form=form)

@app.route("/login")
def get_login_form():
    



# --------------------------------------