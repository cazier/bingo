#!/bin/sh

set -e

. /venv/bin/activate

exec gunicorn bingo.web:app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:5000
