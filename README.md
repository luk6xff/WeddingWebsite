# WeddingWebsite
My wedding website


## Environment setup
* Install python 3.6 
* $ python3 -m venv venv
* $ source venv/bin/activate 
* $ pip install Django==2.0.5
* $ pip install gunicorn


## Application setup
* $ cd weddingwebsite
* $ python manage.py makemigrations
* $ python manage.py migrate
* $ python manage.py collectstatic

##Test the app: 
* $ python manage.py runserver 
* OR
* $ gunicorn weddingwebsite.wsgi
* goto: *localhost:8000*