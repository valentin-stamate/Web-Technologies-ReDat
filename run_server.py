import os

# os.system("pipenv shell")
os.system("gunicorn controller:app --reload")
