from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from app import db, login_manager
from app.entries.utils import decrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    entries = db.relationship("Entry", backref="owner", cascade="all", lazy=True)

    def __repr__(self):
        return f"{self.name} <{self.email}>"


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    url = db.Column(db.String(120), nullable=False)
    notes = db.Column(db.String(1000), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "name", name="user_entries"),)

    def __repr__(self):
        return f"{self.name} <{self.username}>"


    def prettify(self):
        return {
                "ID": self.id,
                "Name": self.name,
                "Last Modified": self.last_modified.strftime('%d-%m-%Y %H:%M:%S'),
                "Username": self.username,
                "Password": decrypt(self.password).decode("utf-8"),
                "URL": self.url,
                "Notes": self.notes,
                }
