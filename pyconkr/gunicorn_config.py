daemon = True
bind = 'unix:/engn001/news_venv/run/gunicorn.sock pyconkr.wsgi:application'
workers = 5
