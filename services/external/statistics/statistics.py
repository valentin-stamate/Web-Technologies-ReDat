import time

import matplotlib.pyplot as plt

from services.external.reddit_api.reddit_data import *
from util.util import current_timestamp

topics = ['Activism',
          'AddictionSupport',
          'Animals',
          'Pets',
          'Anime',
          'Art',
          'Beauty', 'Makeup',
          'Business', 'Economics', 'Finance',
          'Careers',
          'Cars', 'MotorVehicles',
          'Celebrity',
          'Crafts',
          'DIY',
          'Crypto',
          'Culture', 'Ethnicity',
          'Ethics', 'Philosophy',
          'Family', 'Relationships',
          'Fashion',
          'Fitness', 'Nutrition',
          'Food',
          'Funny',
          'Humor',
          'Gaming',
          'Gender',
          'History',
          'Hobbies',
          'Home', 'Garden',
          'Internet', 'Culture', 'Memes',
          'Law',
          'Education',
          'Marketplace', 'Deals',
          'MatureThemes',
          'MentalHealth',
          'MensHealth',
          'Meta',
          'Military',
          'Movies',
          'Music',
          'Outdoors', 'Nature',
          'Place',
          'Podcasts', 'Streamers',
          'Politics',
          'Programming',
          'Reading', 'Writing',
          'Religion', 'Spirituality',
          'Science',
          'SexualOrientation',
          'Sports',
          'TabletopGames',
          'Technology',
          'Television',
          'TraumaSupport',
          'Travel',
          'WomensHealth',
          'WorldNews']


def statistics_thread():
    while True:
        ups_stats = {}
        for topic in topics:
            ups_stats[topic] = 0
            try:
                res = get_hot_posts(topic=topic, limit=100)
                for post in res:
                    ups_stats[topic] = ups_stats[topic] + post['data']['ups']
            except:
                print(topic)
        mark_list = sorted(ups_stats.items(), key=lambda x: x[1], reverse=True)
        sorted_ups_stats = dict(mark_list)
        plt.figure(figsize=(15, 8))
        keys = list(sorted_ups_stats.keys())[0:10]
        values = list(sorted_ups_stats.values())[0:10]
        plt.bar(keys, values, color='orange')
        plt.title("Most up voted 10 subreddits")
        plt.ylabel("Up Votes")
        plt.xlabel("Subreddits")
        plt.savefig("static/stats/ups_stats.png")
        plt.show()
        print("Last updated : " + str(current_timestamp()))
        time.sleep(3600)
