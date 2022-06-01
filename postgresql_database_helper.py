import psycopg2
import sys

def get_db_connection():
    try:
        db_conn.execute('select 1')
    except:
        db_conn = psycopg2.connect(
            database = '<databaseName>',
            user     = 'postgres',
            password = '<password>',
            host     = '<hostName>',
            port     = 5432
        )
        return db_conn


def execute_read(query):
    print('READ: ' + query)
    db_conn = get_db_connection()
    db_cursor = db_conn.cursor()
    db_cursor.execute(query)
    res = db_cursor.fetchall()
    db_conn.commit()
    db_cursor.close()
    return res


def execute_update(query):
    print('UPDATE: ' + query)
    db_conn = get_db_connection()
    db_cursor = db_conn.cursor()
    db_cursor.execute(query)
    db_conn.commit()
    res = db_cursor.rowcount
    db_cursor.close()
    return res

db_conn = get_db_connection()
