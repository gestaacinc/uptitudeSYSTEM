from app import create_app
from app.extensions import db
from flask_migrate import Migrate
import socket

app = create_app()
migrate = Migrate(app, db)
 

if __name__ == "__main__":
    # Get your device's local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    # Run the Flask app and bind it to the local IP address
    app.run(host=local_ip, port=5000, debug=True)
