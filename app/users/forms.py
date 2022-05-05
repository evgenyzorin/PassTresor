from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class SignupForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    name = StringField("Your Name", validators=[DataRequired()])
    password = PasswordField("Master Password", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField("Re-type Master Password", validators=[DataRequired(), EqualTo("password")])

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email address is already taken.")


class SigninForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Master Password", validators=[DataRequired()])
    remember = BooleanField("Remember email")


class ChangeNameForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    name_submit = SubmitField("Change Name")


class ChangeEmailForm(FlaskForm):
    email = StringField("New Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Master Password", validators=[DataRequired()])
    email_submit = SubmitField("Change Email Address")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Email Address is already taken.")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Current Master Password", validators=[DataRequired()])
    new_password = PasswordField("New Master Password", validators=[DataRequired(), Length(min=8)])
    new_password_confirm = PasswordField("Re-type New Master Password", validators=[DataRequired(), EqualTo("new_password")])
    password_submit = SubmitField("Change Master Password")


class DeleteAccountForm(FlaskForm):
    password = PasswordField("Master Password", validators=[DataRequired()])
    delete_submit = SubmitField("Delete")
