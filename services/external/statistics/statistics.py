import time
import matplotlib.pyplot as plt
import numpy as np

from util.external.topics import topics
from services.external.controllers import write_to_csv, matrix_shift
from services.external.reddit_api.reddit_data import *
from util.util import current_timestamp

time_ax = np.arange(10, 70, 10)


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
        plt.savefig("static/stats/general_ups_stats.svg")
        plt.close('all')
        print("(General up votes statistic) Last updated : " + str(current_timestamp()))
        time.sleep(3600)


def comments_statistic():
    comment_stats = [[0] * 6 for i in range(len(topics))]
    while True:
        for topic in topics:
            try:
                res = get_hot_posts(topic=topic, limit=1000)
                for post in res:
                    comment_stats[topics.index(topic)][5] += post['data']['num_comments']
            except Exception:
                print(topic)

        write_to_csv('static/stats/csv/comments.csv', comment_stats)
        matrix_shift(comment_stats, len(topics))
        time.sleep(600)


def upvote_ratio_statistic():
    upvote_ratio_stats = [[0] * 6 for i in range(len(topics))]
    while True:
        for topic in topics:
            try:
                res = get_hot_posts(topic=topic, limit=1000)
                for post in res:
                    upvote_ratio_stats[topics.index(topic)][5] += post['data']['upvote_ratio']
                upvote_ratio_stats[topics.index(topic)][5] /= len(res)
            except Exception:
                print(topic)
        write_to_csv('static/stats/csv/upvote_ratio.csv', upvote_ratio_stats)
        matrix_shift(upvote_ratio_stats, len(topics))
        time.sleep(600)


def ups_downs_statistic():
    ups_stats = [[0] * 6 for i in range(len(topics))]
    downs_stats = [[0] * 6 for i in range(len(topics))]
    while True:
        for topic in topics:
            try:
                res = get_hot_posts(topic=topic, limit=1000)
                for post in res:
                    ups_stats[topics.index(topic)][5] += post['data']['ups']
                    downs_stats[topics.index(topic)][5] += int(post['data']['ups'] / post['data']['upvote_ratio'] -
                                                               post['data']['ups'])
            except Exception:
                print(topic)

        write_to_csv('static/stats/csv/ups.csv', ups_stats)
        write_to_csv('static/stats/csv/downs.csv', downs_stats)
        matrix_shift(ups_stats, len(topics))
        matrix_shift(downs_stats, len(topics))
        time.sleep(600)
