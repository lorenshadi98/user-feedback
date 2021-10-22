"""User feedback application."""

import os
import re
from flask import Flask, redirect, render_template, session, flash
from models import Feedback, db, connect_db, User, Feedback
from forms import UserRegisterForm, UserLoginForm, AddFeedbackForm, EditFeedbackForm
# Application and DB configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Secret key generation for using flash()

app.config['SECRET_KEY'] = 'adsaoij4o43u340'

# database connection and creation
connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    """Home redirect to register user"""
    if "user_username" not in session:
        return redirect("/register")
    user = User.query.get_or_404(session["user_username"])
    return redirect(f"/users/{user.username}")


@app.route("/register", methods=["GET", "POST"])
def user_register_page():
    """Handle user registration"""
    if "user_username" in session:
        return redirect("/")
    form = UserRegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user_login = User.register(username, password)
        new_user = User(username=new_user_login.username, password=new_user_login.password,
                        email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        session["user_username"] = new_user.username
        return redirect("/")
    return render_template("registration-form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def user_login_page():
    """Handle user registration"""
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session["user_username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username or password"]
    return render_template("login-form.html", form=form)


@app.route("/users/<username>")
def profile_page(username):
    """Show secret page"""
    if "user_username" not in session:
        flash("You must be logged in to view this page!", 'danger')
        return redirect("/")
    else:
        user = User.query.filter(User.username == username).first()
        return render_template("user-profile-page.html", user=user)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_username")

    return redirect("/")


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if session["user_username"] == username:
        User.query.filter(User.username == username).delete()
        db.session.commit()
        session.pop("user_username")
        return redirect('/')
    else:
        flash("You must be logged in to view this page!", 'danger')
        return redirect("/")
# ====================== Feedback routes ====================


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Handle new feedback from user"""
    if "user_username" not in session:
        flash("You must be logged in to view this page!", 'danger')
        return redirect("/")
    else:
        form = AddFeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(
                title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{username}")
        return render_template("add-feedback-form.html", form=form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Handle update feedback from user"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if session["user_username"] != feedback.username:
        flash("You are not authorized to do this action", 'danger')
        return redirect("/")
    else:
        form = EditFeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            return redirect("/")
        return render_template("edit-feedback-form.html", form=form)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Handle new feedback from user"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if session["user_username"] != feedback.username:
        flash("You are not authorized to do this action", 'danger')
        return redirect("/")
    else:
        Feedback.query.filter(Feedback.id == feedback_id).delete()
        db.session.commit()
        return redirect("/")
