import os

# os.system("pipenv shell")
os.system("gunicorn server:app --reload")
