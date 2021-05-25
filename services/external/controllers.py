import csv
from io import BytesIO

import numpy as np
from matplotlib import pyplot as plt

from services.external.reddit_api.reddit_data import get_hot_posts
from services.external.topics import topics

time_ax = np.arange(10, 70, 10)


def matrix_shift(matrix, length):
    for row in range(0, length):
        for col in range(1, 6):
            matrix[row][col - 1] = matrix[row][col]
        matrix[row][5] = 0


def write_to_csv(path, rows):
    file = open(path, 'w')
    writer = csv.writer(file)
    writer.writerow(['60 min', '50 min', '40 min', '30 min', '20 min', '10 min'])
    writer.writerows(rows)
    file.close()


def get_general_statistic():
    f = open('static/stats/general_ups_stats.svg', encoding='UTF8')
    return f.read()


def get_upvote_ratio_statistic(topic):
    f = open('static/stats/csv/upvote_ratio.csv', encoding='UTF8')
    csv_reader = csv.reader(f)
    line_nr = 0
    ratio_string = []
    for line in csv_reader:
        if line_nr == topics.index(topic) + 1:
            ratio_string = line
        line_nr += 1
    ratio = []
    for x in ratio_string:
        ratio.append(float(x))
    file = BytesIO()

    plt.figure(figsize=(15, 8))
    fig, ax = plt.subplots()
    ax.bar(time_ax, ratio, color='orange',width=5)
    ax.set(xlabel='time (m)', ylabel='Upvote Ratio',
           title='Upvote ratio in the last hour in {topic}'.format(topic=topic))
    plt.savefig(file, format="svg")
    plt.close('all')
    return file.getvalue()


def get_comments_statistic(topic):
    f = open('static/stats/csv/comments.csv', encoding='UTF8')
    line_nr = 0
    csv_reader = csv.reader(f)
    values_string = []
    for line in csv_reader:
        if line_nr == topics.index(topic) + 1:
            values_string = line
        line_nr += 1
    values = []
    for x in values_string:
        values.append(float(x))
    file = BytesIO()
    plt.figure(figsize=(15, 8))
    fig, ax = plt.subplots()
    ax.plot(time_ax, values)
    ax.set(xlabel='time (m)', ylabel='Nr Comments',
           title='Comments in the last hour in {topic}'.format(topic=topic))
    ax.grid()
    plt.savefig(file, format='svg')
    plt.close('all')
    return file.getvalue()


def get_ups_downs_statistic(topic):
    f = open('static/stats/csv/ups.csv', encoding='UTF8')
    csv_reader = csv.reader(f)
    line_nr = 0
    ups_string = []
    for line in csv_reader:
        if line_nr == topics.index(topic) + 1:
            ups_string = line
        line_nr += 1

    f = open('static/stats/csv/downs.csv', encoding='UTF8')
    csv_reader = csv.reader(f)
    line_nr = 0
    downs_string = []
    for line in csv_reader:
        if line_nr == topics.index(topic) + 1:
            downs_string = line
        line_nr += 1
    ups = []
    downs = []
    for x in ups_string:
        ups.append(float(x))
    for x in downs_string:
        downs.append(float(x))

    file = BytesIO()
    plt.figure(figsize=(15, 8))
    fig, ax = plt.subplots()
    nr_ups = int(ups[0] + ups[1] + ups[2] + ups[3] + ups[4] + ups[5])
    nr_downs = int(downs[0] + downs[1] + downs[2] + downs[3] + downs[4] + downs[5])
    ax.pie([nr_ups, nr_downs], labels=['Up votes ({nr})'.format(nr=nr_ups), 'Down votes ({nr})'.format(nr=nr_downs)])
    ax.set(title='Ups-Downs in the last hour in {topic}'.format(topic=topic))
    plt.legend(title="Votes {nr}".format(nr=nr_ups + nr_downs))
    fig.savefig(file, format='svg')
    plt.close('all')
    return file.getvalue()


def clean_svg(svg: str):
    svg = svg[2:len(svg) - 1:]
    svg = svg.replace("\\n", "")
    return svg


def get_csv_data(path):
    f = open(path, encoding='UTF8')
    csv_reader = csv.reader(f)
    data = "Topic,"
    index = 0
    top = next(csv_reader)
    for time in top:
        data += time + ','
    data = data[:len(data) - 1:]
    data += "\n"
    for line in csv_reader:
        data += topics[index] + ','
        index += 1
        for value in line:
            data += value + ','
        data = data[:len(data) - 1:]
        data += "\n"
    return data


def get_com_nr(topic):
    posts = get_hot_posts(topic, limit=1000)
    com_nr = 0
    for post in posts:
        com_nr += post['data']['num_comments']
    return com_nr


def get_topics():
    data = ''
    for topic in topics:
        data += topic + ','
    data = data[:len(data) - 1:]
    return data
