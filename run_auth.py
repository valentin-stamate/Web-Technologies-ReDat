import os

os.system("gunicorn services.auth.main:app -b :8002 --reload")
