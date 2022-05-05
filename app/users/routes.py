from flask import Blueprint, render_template, url_for, flash, redirect, session
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User
from app.users.forms import (
                            ChangeEmailForm,
                            DeleteAccountForm,
                            SignupForm,
                            SigninForm,
                            ChangeNameForm,
                            ChangePasswordForm,
                            )


users = Blueprint("users", __name__)


@users.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(email=form.email.data, name=form.name.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account has been successfully created.", "success")
        return redirect(url_for("users.signin"))
    return render_template("signup.html", title="Sign Up", form=form)


@users.route("/signin", methods=["GET", "POST"])
def signin():
    session.permanent = True
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("main.index"))
        else:
            flash("Email Address or Master Password is incorrect.", "danger")
    return render_template("signin.html", title="Sign In", form=form)


@users.route("/signout")
def signout():
    logout_user()
    return redirect(url_for("users.signin"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    name_form = ChangeNameForm()
    if name_form.name_submit.data and name_form.validate():
        current_user.name = name_form.name.data
        db.session.commit()
        flash("Name has been successfully changed.", "success")
        return redirect(url_for("users.account"))
    email_form = ChangeEmailForm()
    if email_form.email_submit.data and email_form.validate():
        if bcrypt.check_password_hash(current_user.password, email_form.password.data):
            current_user.email = email_form.email.data
            db.session.commit()
            flash("Email has been successfully changed.", "success")
            return redirect(url_for("users.account"))
        else:
            flash("Master Password is incorrect.", "danger")
    password_form = ChangePasswordForm()
    if password_form.password_submit.data and password_form.validate():
        if bcrypt.check_password_hash(
            current_user.password, password_form.old_password.data
        ):
            current_user.password = bcrypt.generate_password_hash(
                password_form.new_password.data
            ).decode("utf-8")
            db.session.commit()
            flash("Master Password has been successfully changed.", "success")
            return redirect(url_for("users.account"))
        else:
            flash("Master Password is incorrect.", "danger")
    delete_form = DeleteAccountForm()
    if delete_form.delete_submit.data and delete_form.validate():
        if bcrypt.check_password_hash(current_user.password, delete_form.password.data):
            db.session.delete(current_user)
            db.session.commit()
            flash("Account has been successfully deleted.", "success")
            return redirect(url_for("users.signin"))
        else:
            flash("Master Password is incorrect.", "danger")
    return render_template(
                        "account.html",
                        title="My Account",
                        name_form=name_form,
                        email_form=email_form,
                        password_form=password_form,
                        delete_form=delete_form,
                        )
