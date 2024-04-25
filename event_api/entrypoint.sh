#!/bin/sh

set -e

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker -b 0.0.0.0:8000