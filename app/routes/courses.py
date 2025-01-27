from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Course
from app.extensions import db
from fuzzywuzzy import fuzz
from sqlalchemy import func
from flask import jsonify  # Use jsonify to ensure proper JSON response format



bp = Blueprint("courses", __name__, url_prefix="/courses")

@bp.route("/", methods=["GET"])
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 5
    courses = Course.query.filter_by(active=True).paginate(page=page, per_page=per_page)
    return render_template("courses/index.html", courses=courses)

#ADDING COURSE
@bp.route("/create", methods=["POST"])
def create():
    try:
        # Retrieve form data
        name = request.form.get("name")
        tesda_level = request.form.get("tesda_level")
        duration_days = request.form.get("duration_days")
        training_fee = request.form.get("training_fee")
        assessment = request.form.get("assessment") == "1"  # Convert to Boolean
        assessment_fee = request.form.get("assessment_fee") if assessment else None

        # Validate assessment fee if assessment is selected
        if assessment and not assessment_fee:
            flash("Please provide an assessment fee for courses with in-house assessment.", "danger")
            return redirect(url_for("courses.index"))

        # Create and save the course
        new_course = Course(
            name=name,
            tesda_level=tesda_level,
            duration_days=int(duration_days),
            fee=float(training_fee),
            assessment=assessment,
            assessment_fee=float(assessment_fee) if assessment else None,
            active=True  # Explicitly set active to True
        )
        db.session.add(new_course)
        db.session.commit()
        flash("Course added successfully!", "success")
    except Exception as e:
        flash(f"Error adding course: {str(e)}", "danger")

    return redirect(url_for("courses.index"))

# COURSE DUPLICATION VALIDATION
@bp.route("/validate-name", methods=["POST"])
def validate_course_name():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Course name is required."}), 400

        name = data.get("name", "").strip()

        if not name:
            return jsonify({"error": "Course name cannot be empty."}), 400

        # Normalize the input name by removing spaces and converting to lowercase
        normalized_input = name.replace(" ", "").lower()

        # Fetch all course names from the database for comparison
        all_courses = Course.query.with_entities(Course.name).all()
        for course in all_courses:
            db_course_name = course.name.replace(" ", "").lower()

            # Use fuzzy matching to compare course names
            similarity = fuzz.ratio(normalized_input, db_course_name)
            if similarity >= 85:  # Threshold for "close enough"
                return jsonify({"error": f"The course '{name}' is too similar to an existing course."}), 400

        return jsonify({"message": "Course name is available."}), 200

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


# UPDATING COURSE
@bp.route("/update", methods=["POST"])
def update():
    try:
        course_id = request.form.get("id")
        course = Course.query.get_or_404(course_id)

        # Update course details
        course.name = request.form.get("name")
        course.tesda_level = request.form.get("tesda_level")
        course.duration_days = int(request.form.get("duration_days"))
        course.fee = float(request.form.get("training_fee"))
        course.assessment = request.form.get("assessment") == "1"  # Convert to Boolean
        course.assessment_fee = float(request.form.get("assessment_fee")) if course.assessment else None

        db.session.commit()
        flash("Course updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating course: {str(e)}", "danger")

    return redirect(url_for("courses.index"))

# ARCHIVING COURSE
@bp.route("/archive/<int:course_id>", methods=["POST"])
def archive(course_id):
    course = Course.query.get_or_404(course_id)
    course.active = False
    db.session.commit()
    flash(f"The course '{course.name}' has been archived.", "success")
    return redirect(url_for("courses.index"))


