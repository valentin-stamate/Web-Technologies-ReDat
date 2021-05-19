import os
# os.system("pipenv shell")
import threading

from services.external.statistics.statistics import *

x = threading.Thread(target=general_up_votes_statistic, daemon=True)
y = threading.Thread(target=subreddit_comment_stats, daemon=True)
x.start()
y.start()
os.system(""
          "gunicorn services.external.reddit_api.main:app -b :8002 --reload"  # EXTERNAL
          )
