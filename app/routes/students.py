# Routes for student management


from flask import Blueprint, jsonify

bp = Blueprint("students", __name__, url_prefix="/students")

@bp.route("/test", methods=["GET"])
def index():
    return jsonify({"message": "Students route is working!"})
