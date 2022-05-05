import re
import io
import csv
import json
from app import fernet
from flask import make_response, session


def encrypt(message):
    return fernet.encrypt(message)


def decrypt(token):
    return fernet.decrypt(token)


def check_generator(form, label, default):
    if form:
        form_value = form.get(label) if form.get(label) else None
    else:
        form_value = session[label] if label in session else default
    session[label] = form_value
    return form_value


def check_password(password, uppercase, lowercase, digits, symbols):
    uppercase_error = re.search(r"[A-Z]", password) is None if uppercase else False
    lowercase_error = re.search(r"[a-z]", password) is None if lowercase else False
    digit_error = re.search(r"\d", password) is None if digits else False
    symbol_error = re.search(r"[!@#$%^&*]", password) is None if symbols else False
    return not (uppercase_error or lowercase_error or digit_error or symbol_error)


def to_csv(records, filename):
    si = io.StringIO()
    cw = csv.writer(si)
    columns = ["ID", "Name", "Last Modified", "Username", "Password", "URL", "Notes"]
    data = [record.prettify().values() for record in records]
    cw.writerow(columns)
    cw.writerows(data)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={filename}.csv"
    output.headers["Content-type"] = "text/csv"
    return output


def to_json(records, filename):
    data = [record.prettify() for record in records]
    output = make_response(json.dumps(data, indent=4))
    output.headers["Content-Disposition"] = f"attachment; filename={filename}.json"
    output.headers["Content-type"] = "application/json"
    return output
