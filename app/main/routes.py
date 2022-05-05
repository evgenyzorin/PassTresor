from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import current_user
from app.models import Entry
from app.entries.utils import decrypt


main = Blueprint("main", __name__)


@main.route("/")
@main.route("/index")
def index():
    if current_user.is_authenticated:
        search = request.args.get("q", "", type=str)
        page = request.args.get("p", 1, type=int)
        entries = (
                Entry.query.filter_by(owner=current_user)
                .filter(Entry.name.contains(search))
                .order_by(Entry.name.asc())
                .paginate(page=page, per_page=10)
                )
        context = "Entry" if entries.total == 1 else "Entries"
        return render_template("index.html", entries=entries, context=context,
                                search=search, decrypt=decrypt)
    return redirect(url_for("users.signin"))
