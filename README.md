# Stugether: Group Software Engineering Project

Stugether is an appplication to help students reconnect in a blended learning environment. This app aims to create a platform that promotes a better student community, through providing social opportunities and providing infrastructure to help students engage with eachother and foster student community. Some features include daily challenges, being able to post and follow topics as well as engage in community events.

[View web app](https://stugether.herokuapp.com/)

## Running the application
To run the application, first activate virtual environment by typing the following in terminal while being in the same directory as manage.py:
```console
source venv/bin/activate
```
Followed by this command to run a server for the application:
```console
python manage.py startserver 
```
## Alternative method if above fails

First delete old virtual environment by deleting venv folder, then create a 
virtual environment for python 3.7 with the command:
```console
virtualenv -p python3.7 venv
```
Afterwards, activate the virtual environment you just created by running the
following:
```console
source venv/bin/activate
```
Now install requirements in the virtual environment with this command:
```console
pip install -r requirements.txt
```
Finally, type the following to startup the application server:
```console
python3 manage.py runserver
```
## Running with PyCharm
```console
stugether/venv/bin/python
```
## Running tests
```console
python manage.py test
```
