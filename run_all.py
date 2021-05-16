import os
# os.system("pipenv shell")
import threading

from services.external.statistics.statistics import statistics_thread

os.system(""
          "gunicorn services.proxy.main:app -b :8000 --reload | "  # PROXY
          "gunicorn services.auth.main:app -b :8001 --reload |"  # AUTHENTICATION
          "gunicorn services.server.main:app -b :8003 --reload"  # SERVER
          )
x = threading.Thread(target=statistics_thread)
x.start()
