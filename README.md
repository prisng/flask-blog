# Flask Blog
Following [Flask's official tutorial](http://flask.pocoo.org/docs/1.0/tutorial/ "Flask") on getting a simple blog up and running. The application features include user sign-up/login and CRUD capabilities for blog posts.

## Getting started

### Prerequisites
- [Python](https://www.python.org/downloads/ "Python") - version 2.7+ (built with 3.6)
- [MySQL](https://www.mysql.com/downloads/ "MySQL") - version 8.0.11 Community Server - GPL
- (Optional) [MySQLWorkbench](https://www.mysql.com/products/workbench/ "MySQLWorkbench") - version 6.3
- [Flask](http://flask.pocoo.org "Flask") - micro web framework for Python
- [Jinja2](http://jinja.pocoo.org "Jinja2") - template engine for Python

### Flask Setup
1. Create a project directory, "Flask Blog". Create a virtual environment within the project folder:
```
python3 -m venv venv
``` 
2. Activate the environment:
```
. venv/bin/activate
```
3. Install Flask:
```
pip install Flask
```
4. Install the Flask extension which allows MySQL database access: http://flask-mysql.readthedocs.io/en/latest/
```
pip install flask-mysql
```
5. To run the application on your local machine in development mode,
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Replace app.py with the name of your app. Navigate to http://127.0.0.1:5000/ and ta-da. ctrl + c to stop the app.