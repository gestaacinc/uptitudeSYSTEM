
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.extensions import db,bcrypt


# Table: users
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('admin', 'moderator', name='user_roles'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)


# Table: roles
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)
    permissions = db.Column(db.Text, nullable=False)

# Table: students
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    contact_number = db.Column(db.String(15))
    address = db.Column(db.Text)  # Add this field
    status = db.Column(db.Enum('scholarship', 'regular', name='student_status'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

     # One-to-One Relationship with Address
    address = db.relationship("Address", back_populates="student", uselist=False, cascade="all, delete-orphan")


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)
    house_number = db.Column(db.String(50))
    street_address = db.Column(db.String(100))
    barangay = db.Column(db.String(100))
    municipality = db.Column(db.String(100))
    region = db.Column(db.String(100))
    country = db.Column(db.String(100), default="Philippines")  # Default to "Philippines"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # One-to-One Relationship with Student
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), unique=True, nullable=False)
    student = db.relationship("Student", back_populates="address")

# Table: courses
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tesda_level = db.Column(db.Enum('NC I', 'NC II', 'NC III', name='tesda_levels'), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    fee = db.Column(db.Numeric(10, 2), nullable=False)
    assessment = db.Column(db.Boolean, default=False)
    assessment_fee = db.Column(db.Numeric(10, 2))
    active = db.Column(db.Boolean, default=True)  # Set default value to True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



# Table: enrollments
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('enrolled', 'completed', 'dropped', name='enrollment_status'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('enrollments', lazy=True))
    course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))

# Table: payments
class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.Enum('downpayment', 'second', 'third', name='payment_types'), nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False)

    enrollment = db.relationship('Enrollment', backref=db.backref('payments', lazy=True))

# Table: documents
class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('documents', lazy=True))

# Table: activity_logs
class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))
 
