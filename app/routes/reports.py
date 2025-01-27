from flask import Blueprint, render_template

bp = Blueprint("reports", __name__, url_prefix="/reports")

@bp.route("/", methods=["GET"])
def index():
    return render_template("reports/index.html")  # Adjust template path as necessary
