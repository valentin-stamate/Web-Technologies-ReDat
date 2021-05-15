import os

os.system("gunicorn services.server.main:app -b :8003 --reload")
