from flask_wtf import FlaskForm
from wtforms import (IntegerField, StringField, PasswordField,
                    BooleanField, TextAreaField, SelectField)
from wtforms.validators import DataRequired, Length, URL


class EntryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    url = StringField("URL", validators=[DataRequired(), URL()])
    notes = TextAreaField("Notes")
    

class GeneratorForm(FlaskForm):
    password = TextAreaField("Generated Password")
    length = IntegerField("Password Length")
    uppercase = BooleanField("Uppercase Letters (A-Z)")
    lowercase = BooleanField("Lowercase Letters (a-z)")
    digits = BooleanField("Digits (0-9)")
    symbols = BooleanField("Symbols (!@#$%^&*)")


class ExportForm(FlaskForm):
    file_format = SelectField("File Format", choices=[("csv", "csv"), ("json", "json")])
    password = PasswordField("Master Password", validators=[DataRequired()])
