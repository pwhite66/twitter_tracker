# README #

### Required Libraries ###

* Django 1.11.4
* tweepy 3.5.0
* django-picklefield 1.0.0

* Twitter app api credential
* Google map api key

### Additional Functionality ###

Additional GET response has been added
* "handle" handle will allow the ability to override the default account
* "count" count allows the modification of the number displayed tweets


### Initialize Project ###

To initialize the project either run the start_server.sh script or call python manage.py runserver in the command line

The url to the project is 127.0.0.1:8000

To change the handle and count the url is 127.0.0.1:8000/?handle=@MaplecroftRisk&count=12
