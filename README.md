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
* $ python manage.py collectstatic --noinput --clear
* $ django-admin makemessages
* $ django-admin compilemessages

##Test the app: 
* $ python manage.py runserver 80
* OR
* $ gunicorn -d -b 0.0.0.0:80 weddingwebsite.wsgi
* goto: *localhost:80*

## Run the app with NGINX
1. Install nginx:
* $ sudo apt install nginx
2. Create a config Nginx file:
$ touch /etc/nginx/sites-available/weddingwebsite
`
server {
    listen 80;
    server_name 0.0.0.0;

    location = /static/favicon.ico { access_log off; log_not_found off; }

    #For favicon
    location  /favicon.ico {
        alias ~/WeddingWebsite/weddingwebsite/static_root/favicon.ico;
    }
    #For robots.txt
    location  /robots.txt {
        alias ~/WeddingWebsite/weddingwebsite/static_root/robots.txt ;
    }
    
    # Error pages
    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root ~/WeddingWebsite/weddingwebsite/static_root/;
    }

    location /static/ {
        autoindex on;
        root ~/WeddingWebsite/weddingwebsite/static_root/;
    }

    location /media/ {
        autoindex on;
        root ~/WeddingWebsite/weddingwebsite/media/;
    }

    location / {
            include proxy_params;
            proxy_pass http:~/WeddingWebsite/weddingwebsite/weddingwebsit.sock;
    }
`
3. Link this file to the sites-enabled Nginx folder:
* $ sudo ln -s /etc/nginx/sites-available/weddingwebsite /etc/nginx/sites-enabled

4. Check if created configuratin does not contain any bugs by typing:
* $ sudo nginx -t
If all is ok, you should see similar info:
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

5. Modify a gunicorn run command to be able to talk to Nginx:
* $ gunicorn --daemon --workers=5 --bind unix:~/WeddingWebsite/weddingwebsite/weddingwebsit.sock weddingwebsite.wsgi
OR
6. Run gunicorn_run.sh script:
$ ./WeddingWebsite/weddingwebsite/gunicorn_run.sh

7. Restart Nginx:
$ systemctl restart nginx
... and go to 0.0.0.0:80. The app shoul be running smoothly right now : )
