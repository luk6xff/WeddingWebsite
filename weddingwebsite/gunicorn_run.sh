#!/bin/bash
# Script based on: https://hackernoon.com/deploy-django-app-with-nginx-gunicorn-postgresql-supervisor-9c6d556a25ac

NAME="weddingwebsite"                                       # Name of the application (*)
APP_DIR=~/WeddingWebsite/weddingwebsite/                    # WeddingWebsite project directory (*)
SOCKFILE=~/WeddingWebsite/weddingwebsite/weddingwebsit.sock # we will communicate using this unix socket (*)
USER=root                                                   # the user to run as (*)
GROUP=webdata                                               # the group to run as (*)
NUM_WORKERS=5                                               # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=weddingwebsite.settings              # which settings file should Django use (*)
DJANGO_WSGI_MODULE=weddingwebsite.wsgi                      # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $APP_DIR
source ../venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$APP_DIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# If program is meant to be run under supervisor, it shall not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --daemon
    --name $NAME \
    --workers $NUM_WORKERS \
    --user $USER \
    --bind=unix:$SOCKFILE