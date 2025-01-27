set FLASK_APP=run.py
set FLASK_ENV=development
flask db init
flask db migrate -m "Initial migration"
flask db upgrade


