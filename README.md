# WeddingWebsite
My wedding website


## Environment setup
* Install python 3.6 
* $ python3 -m venv venv
* $ source venv/bin/activate 
* $ cd weddingwebsite
* $ pip install -r requirements.txt


## Application setup
* $ cd weddingwebsite
* $ python manage.py migrate
* $ python manage.py makemigrations
* $ python manage.py createsuperuser
* $ python manage.py collectstatic
* $ django-admin makemessages
* $ django-admin compilemessages

##Test the app: 
* $ python manage.py runserver 80
* OR
* $ gunicorn weddingwebsite.wsgi
* goto: *localhost:80*
