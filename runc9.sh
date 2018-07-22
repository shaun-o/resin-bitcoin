redis-server &
export redis=localhost
cd src
celery worker -A main.celery -l debug
