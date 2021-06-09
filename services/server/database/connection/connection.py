import psycopg2


def execute_sql(sql: str, parameters=()):
    connection = psycopg2.connect(database='redat', user='postgres', password='postgres', host='127.0.0.1', port='5432')
    cursor = connection.cursor()

    cursor.execute(sql, parameters)

    try:
        rows = cursor.fetchall()
    except:
        rows = []

    cursor.close()
    connection.commit()
    connection.close()
    return rows
