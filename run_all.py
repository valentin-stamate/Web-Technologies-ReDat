import os
# os.system("pipenv shell")
import threading

from services.external.statistics.statistics import general_up_votes_statistic

os.system(""
          "gunicorn services.proxy.main:app -b :8000 --reload | "  # PROXY
          "gunicorn services.auth.main:app -b :8001 --reload |"  # AUTHENTICATION
          "gunicorn services.external.main:app -b :8002 --reload"  # EXTERNAL
          "gunicorn services.server.main:app -b :8003 --reload"  # SERVER
          )
x = threading.Thread(target=general_up_votes_statistic)
x.start()
