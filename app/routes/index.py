from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User
from app.extensions import db

bp = Blueprint("index", __name__, url_prefix="/")

@bp.route("/", methods=["GET", "POST"])
def index():
    print(f"App context active: {db.engine}")  # Debug log to check db initialization

    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate credentials
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Store user details in the session
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("index.html")
