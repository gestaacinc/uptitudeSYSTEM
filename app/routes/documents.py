# Routes for document uploads


from flask import Blueprint, jsonify

bp = Blueprint("documents", __name__, url_prefix="/documents")

@bp.route("/test", methods=["GET"])
def index():
    return jsonify({"message": "Documents route is working!"})
