release: python manage.py migrate
web: gunicorn SmrtSummary.wsgi --log-file -
worker: python manage.py rqworker default
