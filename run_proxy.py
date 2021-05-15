import os

os.system("gunicorn services.proxy.main:app -b :8000 --reload")
