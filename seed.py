from app import create_app
from app.extensions import db
from app.models import User

# Create the Flask app instance
app = create_app()

# Run the script in the app context
with app.app_context():
    # Check if the user already exists to avoid duplicate entries
    if not User.query.filter_by(username="admin").first():
        # Create a test user
        test_user = User(
            username="admin",
            email="admin@example.com",
            role="admin"
        )
        test_user.set_password("adminpass")  # Hash the password
        db.session.add(test_user)
        db.session.commit()

        print("Test user added successfully!")
    else:
        print("Test user already exists.")
