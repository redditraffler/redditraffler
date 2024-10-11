web: newrelic-admin run-program gunicorn --bind 0.0.0.0:${PORT} runserver:app & flask rq worker
release: ./release_tasks.sh
