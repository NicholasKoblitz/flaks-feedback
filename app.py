
from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, User
from forms import CreateUserForm, LoginUserForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "quiinnfhyeteenhcllskjf7199275364l"
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

@app.route("/login", methods=["GET", "POST"])
def get_login_form():
    """Gets the login form"""

    form = LoginUserForm()

    if form.validate_on_submit():

        username =form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            redirect("/secret")
        else:
            flash("Wrong username/password")
        

    return render_template("login.html", form=form)


@app.route("/logout", methods=["POST"])
def logout_user():
    """Logs the user out"""

    session.pop("username")

    return redirect("/login")


@app.route("/secret")
def get_secret_page():
    """Gets the secret web page"""

    if "username" not in session:
        flash("Please Login In")
        return redirect("/login")
    else:
        return render_template("secret.html")


# --------------------------------------