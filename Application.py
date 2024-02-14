from flask import Flask, jsonify, request, abort
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import database_exists, create_database
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import jwt
import re
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/user_databse'
secret = app.config['SECRET_KEY'] = 'C0nnecttowebApp'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

with app.app_context():
    db.create_all()
@app.route('/registeruser')
def register_user():
    data = request.get_json()
    email = data.get('username')  
    password = data.get('password')

    # Check if email is in a valid format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'message': 'Invalid email format'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login')
def login():
    data = request.get_json()
    email = data.get('username')  
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Could not verify user', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    user = User.query.filter_by(username=email).first()

    if not user:
        return jsonify({'message': 'User not found', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    if bcrypt.check_password_hash(user.password, password):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret)
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split()[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, secret, algorithms=['HS256'])
            current_user = User.query.filter_by(username=data['username']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def check_database():
    try:
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        engine = create_engine(database_uri)
        
        if not database_exists(engine.url):
            create_database(engine.url)
            print("Database 'user_database' created successfully.")
        else:
            print("Database 'user_database' already exists.")

    except OperationalError as e:
        print("Error creating database:", str(e))

check_database()

@app.route('/healthz', methods=['HEAD', 'OPTIONS'])
def handle_invalid_methods():
    return jsonify(message="Method Not Allowed"), 405

@app.route('/healthz', methods=['GET'])
@token_required
def health_check_database(current_user):
    if request.method != 'GET':
        abort(405)
    try:
        print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])
        print("Executing database query.......")
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        with engine.connect() as connection:
            query = text('SELECT 1;')
            result = connection.execute(query)
            print("Query Executed!")
            # Fetching result is optional, but you can do so if needed
            result.fetchone()

        response = jsonify(status='ok', message='OK')
        response.status_code = 200
        response.headers['Cache-Control'] = 'no-cache'
        return response
    except OperationalError as e:
        print(f"Error executing database query: {str(e)}")
        error_response = jsonify(status='error', message='Service Unavailable')
        error_response.status_code = 503
        error_response.headers['Cache-Control'] = 'no-cache'
        return error_response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    
#REFERENCES
#API — Flask Documentation (3.0.X). (n.d.). https://flask.palletsprojects.com/en/3.0.x/api/
#Flask-SQLAlchemy — Flask-SQLAlchemy Documentation (3.1.x). (n.d.). https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/
#https://www.redhat.com/sysadmin/postgresql-setup-use-cases
#Flask interfaces — API — Flask API. (n.d.). https://tedboy.github.io/flask/interface_api.html
#https://flask-jwt-extended.readthedocs.io/en/stable/custom_decorators.html

