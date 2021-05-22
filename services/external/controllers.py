import csv
from io import BytesIO

import numpy as np
from matplotlib import pyplot as plt

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
        if line_nr == topics.index(topic):
            ratio_string = line
        line_nr += 1
    ratio = []
    for x in ratio_string:
        ratio.append(float(x))
    file = BytesIO()

    plt.figure(figsize=(15, 8))
    fig, ax = plt.subplots()
    ax.stackplot(time_ax, ratio)
    ax.set(xlabel='time (m)', ylabel='Upvote Ratio',
           title='Upvote ratio in the last hour in {topic}'.format(topic=topic))
    ax.grid()
    plt.savefig(file, format="svg")
    plt.close('all')
    return file.getvalue()


def get_comments_statistic(topic):
    f = open('static/stats/csv/comments.csv', encoding='UTF8')
    line_nr = 0
    csv_reader = csv.reader(f)
    values_string = []
    for line in csv_reader:
        if line_nr == topics.index(topic):
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
        if line_nr == topics.index(topic):
            ups_string = line
        line_nr += 1

    f = open('static/stats/csv/downs.csv', encoding='UTF8')
    csv_reader = csv.reader(f)
    line_nr = 0
    downs_string = []
    for line in csv_reader:
        if line_nr == topics.index(topic):
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
    ax.plot(time_ax, ups, color='blue', label='up votes', linewidth=2)
    ax.plot(time_ax, downs, color='red', label='down votes', linewidth=2)
    ax.set(xlabel='time (m)', ylabel='Ups-Downs',
           title='Ups-Downs in the last hour in {topic}'.format(topic=topic))
    ax.grid()
    ax.legend()
    fig.savefig(file, format='svg')
    plt.close('all')
    return file.getvalue()


def clean_svg(svg: str):
    svg = svg[2:len(svg) - 1:]
    svg = svg.replace("\\n", "")
    return svg
