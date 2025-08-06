web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
release: python migrate_production.py
