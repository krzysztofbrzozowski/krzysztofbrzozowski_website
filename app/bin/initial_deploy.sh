#!/usr/bin/env bash

# Verify if prod SECRET_KEY exists
# If does not exist -> autogenerate
secret_key_file=secret_key.txt
if [ ! -f "/app/bin/${secret_key_file}" ]; then
  echo "Secret does not exist, creating new one"
  var=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())' 2>&1)
  echo $var > "/app/bin/${secret_key_file}"
else
  echo "Secret SECRET_KEY exists"
fi

# Do action during initial deploy
if [ "true" == $DO_INITIAL_DEPLOY ]; then
    # Remove sb.sqlite3 dbs
    if [ -f "db.sqlite3" ]; then
        rm *.sqlite3
    fi

    # Create superuser
    python manage.py migrate
    python manage.py createsuperuser --no-input 2>&1
fi