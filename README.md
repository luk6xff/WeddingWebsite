# WeddingWebsite
My wedding website


## Environment setup
* Install python 3.6 
```bash
$ python3 -m venv venv
```
```bash
$ source venv/bin/activate 
```
```bash
$ cd weddingwebsite
```
```bash
$ pip install -r requirements.txt
```

## Application setup
```bash
$ cd weddingwebsite
```
```bash
$ python manage.py migrate
```
```bash
$ python manage.py makemigrations
```
```bash
$ python manage.py createsuperuser
```
```bash
$ python manage.py collectstatic --noinput --clear
```
```bash
$ django-admin makemessages
```
```bash
$ django-admin compilemessages
```
##Test the app: 
* $ python manage.py runserver 80
* OR
```bash
* $ gunicorn -d -b 0.0.0.0:80 weddingwebsite.wsgi

* goto: *localhost:80*

## Run the app with NGINX
1. Install nginx:
```bash
$ sudo apt install nginx
```
2. Create a config Nginx file:
```bash
$ touch /etc/nginx/sites-available/weddingwebsite
```
3. Paste the configuration from `weddingwebsite_nginx.conf` file into the file: `/etc/nginx/sites-available/weddingwebsite`

4. Link this file to the sites-enabled Nginx folder:
```bash
$ sudo ln -s /etc/nginx/sites-available/weddingwebsite /etc/nginx/sites-enabled
```
5. Check if created configuratin does not contain any bugs by typing:
```bash
$ sudo nginx -t
```
If all is ok, you should see similar info:
```bash
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```
6. Modify a gunicorn run command to be able to talk to Nginx:
```bash
$ gunicorn --daemon --workers=5 --bind unix:~/WeddingWebsite/weddingwebsite/weddingwebsite.sock weddingwebsite.wsgi
```
OR
7. Run gunicorn_run.sh script:
```bash
$ sudo chmod u+x gunicorn_run.sh
```
```bash
$ ./gunicorn_run.sh
```

8. Modify ```/etc/nginx/nginx.conf``` as shown below:
```bash
user root www-data
```

9. Restart Nginx:
```bash
$ systemctl restart nginx
```
10. Open 0.0.0.0:80 in the browser, your app should be running smoothly right now : )
