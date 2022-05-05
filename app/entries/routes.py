import secrets
import string
from datetime import datetime
from flask import (Blueprint, render_template, url_for, flash, redirect,
                    request, abort, session)
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from app import db, bcrypt
from app.models import Entry
from app.entries.utils import (encrypt, decrypt, check_generator,
                                check_password, to_csv, to_json)
from app.entries.forms import EntryForm, GeneratorForm, ExportForm


entries = Blueprint("entries", __name__)


@entries.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry(
                    name=form.name.data,
                    username=form.username.data,
                    password=encrypt((form.password.data).encode("utf-8")),
                    url=form.url.data,
                    notes=form.notes.data,
                    owner=current_user,
                    )
        db.session.add(entry)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Entry already exists.", "danger")
            return redirect(url_for("entries.add"))
        flash("Entry has been successfully created.", "success")
        return redirect(url_for("main.index"))
    return render_template("add.html", title="Add Entry", form=form, text="Add Entry")


@entries.route("/edit/<int:entry_id>", methods=["GET", "POST"])
@login_required
def edit(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if entry.owner != current_user:
        abort(403)
    form = EntryForm()
    if request.method == "GET":
        form.name.data = entry.name
        form.username.data = entry.username
        form.password.data = decrypt(entry.password).decode("utf-8")
        form.url.data = entry.url
        form.notes.data = entry.notes
    elif form.validate_on_submit():
        entry.name = form.name.data
        entry.last_modified = datetime.utcnow()
        entry.username = form.username.data
        entry.password = encrypt((form.password.data).encode("utf-8"))
        entry.url = form.url.data
        entry.notes = form.notes.data
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Entry already exists.", "danger")
            return redirect(url_for("entries.edit", entry_id=entry.id))
        flash("Entry has been successfully updated.", "success")
        return redirect(url_for("main.index"))
    return render_template("add.html", title="Edit Entry", form=form, text="Edit Entry")


@entries.route("/delete/<int:entry_id>", methods=["GET", "POST"])
@login_required
def delete(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    if entry.owner != current_user:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry has been successfully deleted.", "success")
    return redirect(url_for("main.index"))


@entries.route("/tools/generator", methods=["GET", "POST"])
@login_required
def generator():
    form = GeneratorForm()
    if request.method == "GET":
        form.length.data = session.get("length", "12")
        form.uppercase.data = session.get("uppercase", "y")
        form.lowercase.data = session.get("lowercase", "y")
        form.digits.data = session.get("digits", "y")
        form.symbols.data = session.get("symbols", None)
    elif request.method == "POST":
        length = int(check_generator(request.form, "length", "12"))
        uppercase = (string.ascii_uppercase
            if check_generator(request.form, "uppercase", "y") else "")
        lowercase = (string.ascii_lowercase
            if check_generator(request.form, "lowercase", "y") else "")
        digits = string.digits if check_generator(request.form, "digits", "y") else ""
        symbols = "!@#$%^&*" if check_generator(request.form, "symbols", None) else ""
        alphabet = uppercase + lowercase + digits + symbols
        try:
            while True:
                password = "".join([secrets.choice(alphabet) for _ in range(length)])
                if (check_password(password, uppercase, lowercase, digits, symbols)):
                    break
            return password
        except IndexError:
            return ""
    return render_template("generator.html", title="Password Generator", form=form)


@entries.route("/tools/export", methods=["GET", "POST"])
@login_required
def export():
    form = ExportForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            session["download"] = "csv" if form.file_format.data == "csv" else "json"
            session.pop("csrf_token", None)
            return render_template("export.html", form=form, show_modal=True)
        else:
            flash("Master Password is incorrect.", "danger")
    return render_template("export.html", title="Export Tresor", form=form)


@entries.route("/download", methods=["GET", "POST"])
@login_required
def download():
    records = Entry.query.filter_by(owner=current_user)
    filename = f"passtresor-export-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    try:
        return to_csv(records, filename) if (session.pop("download") == "csv") else to_json(records, filename)
    except KeyError:
        return redirect(url_for("entries.export"))
