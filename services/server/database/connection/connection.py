import psycopg2
from secrets import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def execute_sql(sql: str, parameters=()):
    connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
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
