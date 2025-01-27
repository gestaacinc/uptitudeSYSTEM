from flask import Flask
from app.extensions import db, migrate, bcrypt
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Import and register blueprints
    from app.routes import users, students, courses, enrollments, payments, documents, dashboard, index, reports
    app.register_blueprint(reports.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(students.bp)
    app.register_blueprint(courses.bp)
    app.register_blueprint(enrollments.bp)
    app.register_blueprint(payments.bp)
    app.register_blueprint(documents.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(index.bp)

    return app
