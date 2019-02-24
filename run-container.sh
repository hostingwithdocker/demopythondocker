#!/bin/bash

cd /app
pipenv run gunicorn app:app --bind ${APP_BIND}:8080
