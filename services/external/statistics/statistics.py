import time

import matplotlib.pyplot as plt
import numpy as np

from services.external.reddit_api.reddit_data import *
from util.util import current_timestamp

topics = ['Activism', 'AddictionSupport', 'Animals', 'Anime', 'AskReddit', 'Pets', 'Art', 'Beauty', 'Makeup',
          'Business', 'Economics', 'Finance', 'Careers', 'Cars', 'Celebrity', 'Crafts', 'DIY',
          'Crypto', 'Culture', 'Ethnicity', 'Ethics', 'Philosophy', 'Family', 'Relationships', 'Fashion', 'Fitness',
          'Nutrition', 'Food', 'Funny', 'Humor', 'Gaming', 'Gender', 'History', 'Hobbies', 'Home', 'Garden', 'Internet',
          'Culture', 'Memes', 'Law', 'Education', 'Marketplace', 'Deals', 'MentalHealth', 'MensHealth',
          'Meta', 'Military', 'Movies', 'Music', 'Outdoors', 'Nature', 'Place', 'Podcasts', 'Streamers', 'Politics',
          'Programming', 'Reading', 'Writing', 'Religion', 'Spirituality', 'Science', 'SexualOrientation', 'Sports',
          'TabletopGames', 'Technology', 'Television', 'Travel', 'WorldNews']


def general_up_votes_statistic():
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
        plt.savefig("static/stats/ups_stats.svg")
        plt.show()
        print("(General up votes statistic) Last updated : " + str(current_timestamp()))
        time.sleep(3600)


def matrix_shift(matrix):
    for row in range(0, len(topics)):
        for col in range(1, 6):
            matrix[row][col - 1] = matrix[row][col]
        matrix[row][5] = 0


def subreddit_comment_stats():
    comment_stats = [[0] * 6 for i in range(len(topics))]
    time_ax = np.arange(0, 60, 10)
    while True:
        current_index = 0
        for topic in topics:
            try:
                res = get_hot_posts(topic=topic, limit=10)
                print(topics.index(topic))
                for post in res:
                    comment_stats[topics.index(topic)][5] += post['data']['num_comments']
            except Exception:
                print(topic)
            print(comment_stats[topics.index(topic)])
            plt.figure(figsize=(15, 8))
            fig, ax = plt.subplots()
            ax.plot(time_ax, comment_stats[topics.index(topic)])
            ax.set(xlabel='time (m)', ylabel='nr comments',
                   title='Comments in the last hour in {topic}'.format(topic=topic))
            ax.grid()
            fig.savefig("static/stats/{topic}_stats.svg".format(topic=topic))
            plt.close('all')
            print("({topic} comments statistic) Last updated : ".format(topic=topic) + str(current_timestamp()))

        matrix_shift(comment_stats)
        time.sleep(600)
