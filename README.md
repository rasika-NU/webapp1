**#WEB APPLICATION REQUIREMENTS:**

**Getting Started**
--------------------------------------------------------------------------------------------------------------------------------------------------------

**INSTALL PYTHON VERSION 3 and PIP**

Refer to the documents: 
  - https://www.python.org/downloads/
  - https://pip.pypa.io/en/stable/installation/

Install the required libraries:

  - Flask: The main Flask framework for building web applications.
	- jsonify: A function provided by Flask for returning JSON responses.
	- request: An object provided by Flask for accessing request data.
	- abort: A function provided by Flask for aborting request handling and returning an error response.
	- Flask-Bcrypt: An extension for Flask that provides bcrypt hashing utilities.
	- SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
	- create_engine: Function from SQLAlchemy used to create database engine instances.
	- text: Class from SQLAlchemy used to represent textual SQL constructs.
	- OperationalError: Exception class from SQLAlchemy that represents database operational errors.
	- database_exists: Function from SQLAlchemy-Utils used to check if a database exists.
	- create_database: Function from SQLAlchemy-Utils used to create a database.
	- Flask-SQLAlchemy: An extension for Flask that integrates SQLAlchemy into Flask applications.
	- bcrypt: A library for password hashing using bcrypt algorithm.
	- jwt: A library for encoding and decoding JSON Web Tokens (JWT).
	- re: The Python regular expression module for working with regular expressions.
	- datetime: The Python module for working with dates and times.
	- wraps: A function from the functools module used for creating decorators while preserving function metadata.

Command to install all the dependencies:

- pip install flask flask-bcrypt SQLAlchemy Flask-SQLAlchemy bcrypt jwt SQLAlchemy-Utils

    
Create a postgres database by following below instructions:
  - install postgresql v.16 : https://www.postgresql.org/download/
  - start and enable postgresql service

Make sure the ports 8080 and 54321 are open in firewall:
Command to enable the port on CentOS:
- firewall-cmd --zone=public --add-port=8080/tcp --permanent
- firewall-cmd --zone=public --add-port=54321/tcp --permanent
  
Now once you have completed all the steps:
 - Run the application by using 'Python3 Application.py' command
 - Test all the scenarios.



