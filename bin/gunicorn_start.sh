#!/bin/bash

NAME="GimmeThatDjango"     # Name of project
DJANGODIR=/var/www/gimmeth.at/src   # Django project directory
SOCKFILE=/var/www/gimmeth.at/src/run/gunicorn.sock    # communicate using this unix socket
USER=gimmethat   # the user to run as
GROUP=webapps   # the group to run as
NUM_WORKERS=3   # how many worker processes Gunicorn should spawn =2*cores + 1?
DJANGO_SETTINGS_MODULE=GimmeThatDjango.settings.production  # which settings file should Django user
DJANGO_WSGI_MODULE=GimmeThatDjango.wsgi   # WSGI module name


echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../bin/secrets.sh
source /usr/local/bin/virtualenvwrapper.sh
workon gimmeprodvenv
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves
exec /var/www/gimmeth.at/Envs/gimmeprodvenv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=- \
