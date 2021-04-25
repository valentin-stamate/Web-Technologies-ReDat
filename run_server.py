import os

os.system("gunicorn server:app --reload")
