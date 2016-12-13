Wake N Shake

The smart alarm clock with awesome tunes!

## Table of Contents

* Project Version
* Documentation

## Project Version
Version 1.0 /hacks 2016

## Documentation

This section includes crucial information on how to set up the web application on any server

### Developer Setup

#### Virtual Environment

To install a virtual enviornment, use
	
	``` pip install virtualenv 

In order to run it and install requirements, be in the proper directory and then run
	
	```source venv/bin/activate
	
	``` pip install -r requirements.txt

To end session,
	``` deactivate

#### Running Django

To run development server and migrate models to sqlite3 db
	
	``` python manage.py makemigrations
	
	``` python manage.py migrate
	
	``` python manage.py runserver


#### Adding 12
