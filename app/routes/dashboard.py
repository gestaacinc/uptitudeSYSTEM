# Routes for the admin dashboard

from flask import Blueprint, render_template, session, redirect, url_for, flash, request

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@bp.route("/", methods=["GET"])
def index():
    if "user_id" not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("index.index"))  # Redirect to login if not authenticated


    # Safely fetch username
    username = session.get("username", "Unknown User")

     # Fetch user's IP address
    user_ip = request.remote_addr
    
    return render_template("dasbhoard.html", username=username, user_ip=user_ip)
