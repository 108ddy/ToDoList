#!/usr/bin/env bash

function wait_for_db() {
  echo "Waiting for db connection..."

  while ! nc -z "$DB_HOST" "$DB_PORT";
  do
    sleep 0.1
  done

  echo "DB started."
}

function run_server() {
  echo "Server is starting..."

  wait_for_db

  pending_migrations=$(python manage.py showmigrations | grep '\[ \]' -c)

  if [[ "$pending_migrations" == 0 ]]
  then
    echo "All migration was applied."
  else
    python manage.py migrate
  fi

  create_superuser

  python manage.py runserver 0.0.0.0:8000
}

function create_superuser() {
  echo "Creating superuser..."

  echo "from django.contrib.auth.models import User;" \
    "User.objects.filter(username='$SU_NAME').exists() or" \
    "User.objects.create_superuser('$SU_NAME', '', '$SU_PASSWORD');" | python manage.py shell

  echo "Superuser was created."
}

run_server
