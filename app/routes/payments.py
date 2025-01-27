# Routes for payment management


from flask import Blueprint, jsonify

bp = Blueprint("payments", __name__, url_prefix="/payments")

@bp.route("/test", methods=["GET"])
def index():
    return jsonify({"message": "Payments route is working!"})
