# Routes for enrollment management

from flask import Blueprint, render_template
from app.models import Enrollment, Course  # Import your models
from app.models import Student, Address

bp = Blueprint('enrollments', __name__, url_prefix='/enrollments')

@bp.route("/", methods=["GET"])
def index():
    # Fetch all enrollments
    enrollments = Enrollment.query.all()
    # Fetch all active courses
    courses = Course.query.filter_by(active=True).all()
    return render_template("enrollments/index.html", enrollments=enrollments, courses=courses)


def create_student_with_address(data):
    # Create student
    student = Student(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        contact_number=data["contact_number"],
        status=data["status"],
    )
    db.session.add(student)
    db.session.flush()  # Get the student ID before committing

    # Create address linked to student
    address = Address(
        house_number=data["house_number"],
        street_address=data["street_address"],
        barangay=data["barangay"],
        municipality=data["municipality"],
        region=data["region"],
        country=data.get("country", "Philippines"),
        student_id=student.id,
    )
    db.session.add(address)
    db.session.commit()

    return student