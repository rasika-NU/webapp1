from flask import Flask, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost:5432/user_databse'

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

@app.route('/healthz', methods=['GET'])
def health_check_database():
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

