import os

# os.system("pipenv shell")
os.system("gunicorn services.proxy.main:app --reload")
