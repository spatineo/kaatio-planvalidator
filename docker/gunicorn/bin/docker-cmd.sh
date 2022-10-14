#!/bin/bash

gunicorn kaatio_plan_validator.main:app \
    --bind :8000 \
    --capture-output \
    --access-logfile '-' \
    --error-logfile '-' \
    --workers 3 \
    --worker-class uvicorn.workers.UvicornWorker
