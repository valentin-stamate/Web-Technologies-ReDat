import os

os.system("gunicorn services.auth.main:app -b :8001 --reload")
