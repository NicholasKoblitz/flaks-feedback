from flask import Flask, render_template, redirect, session, flash, request
from models import db, connect_db, User, Feedback
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

        return redirect(f"/users/{user.username}")
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
            return redirect(f"/users/{user.username}")
        else:
            flash("Wrong username/password")

    return render_template("login.html", form=form)




@app.route("/logout", methods=["POST"])
def logout_user():
    """Logs the user out"""

    session.pop("username")

    return redirect("/login")


#? --------------User Routes ----------------------

@app.route("/users/<username>")
def get_user_details(username):

    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter(Feedback.username == user.username).all()

    if "username" not in session:
        flash("Please Login In")
        return redirect("/login")
    else:
        return render_template("user_details.html", user=user, feedback=feedback)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Deletes the given user"""

    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter(Feedback.username == user.username).all()


    if "username" not in session:
        flash("Please Login")
        return redirect("/login")
    else:
        for item in feedback:
            item.query.delete()
        user.query.delete()
        db.session.commit()
        session.pop("username")
        flash("User Deleted")
        return redirect('/')


@app.route("/users/<username>/feedback/add")
def get_feedback_form(username):
    """Gets the feedback form"""

    user = User.query.filter_by(username=username).first()

    
    if "username" not in session:
        flash("Please Login")
        return redirect("/login")
    else:
        return render_template("feedback.html", user=user)


@app.route("/users/<username>/feedback/add", methods=["POST"])
def feedback_form(username):

    user = User.query.filter_by(username=username).first()


    if "username" not in session:

        flash("Please Login")
        return redirect("/login")

    else:

        title = request.form["title"]
        content = request.form["content"]
    
        feedback = Feedback(title=title, content=content, username=user.username)
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{user.username}")
    

#? --------------End of User Routes ----------------------


#* -----------Feedback Routes-----------------

@app.route("/feedback/<int:feedback_id>/update")
def get_feedback_update_form(feedback_id):
    """Gets feedback update form"""

    feedback = Feedback.query.get_or_404(feedback_id)
    return render_template("feedback_update.html", feedback=feedback)



@app.route("/feedback/<int:feedback_id>/update", methods=["POST"])
def update_feedback(feedback_id):
    """Updates a user's feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)

    if "username" not in session:
        flash("Please Login in")
        redirect("/login")
    else:
        title = request.form["title"]
        content = request.form["content"]

        feedback.title = title
        feedback.content = content
        
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.user.username}")


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Deletes user feedback"""

    feedback = Feedback.query.get_or_404(feedback_id)
    user = feedback.user.username

    if "username" not in session:
        flash("Please Login")
        return redirect("/login")
    else:

        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/users/{user}")





#* -------------End Feedback Routes ------------------


# --------------------------------------------------------------------