import os
# os.system("pipenv shell")
import threading

from services.external.statistics.statistics import statistics_thread

x = threading.Thread(target=statistics_thread, daemon=True)
x.start()
os.system(""
          "gunicorn services.external.reddit_api.main:app -b :8002 --reload"  # EXTERNAL
          )
