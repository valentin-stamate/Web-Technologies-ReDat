import psycopg2


def execute_sql(sql):
    connection = psycopg2.connect(database='redat', user='postgres', password='postgres', host='127.0.0.1', port='5432')
    cursor = connection.cursor()

    cursor.execute(sql)

    rows = []
    try:
        rows = cursor.fetchall()
    except:
        rows = []

    connection.commit()
    connection.close()
    return rows
