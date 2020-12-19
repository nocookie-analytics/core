#! /usr/bin/env bash
set -e

python /app/app/celeryworker_pre_start.py

C_FORCE_ROOT=1 celery -A app.worker worker -l info -Q main-queue -c 1
