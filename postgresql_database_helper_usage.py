import boto3
import time

from utils.database_helper import *

def lambda_handler(event, context):

    print(event)

    # INITIAL GET_RECORDS STEPS
    if 'action' in event:
        query = "select ... order by row_id limit 1000"

        rows_to_process = execute_read(query)
        print(query)

        resp = {}
        resp['data'] = []
        resp['count'] = len(rows_to_process)
        for row in rows_to_process:
            resp['data'].append(row[0])

        query = "update ..."

        execute_update(query)

        return resp

    # COMMON FOR EXECUTING QUERIES
    elif 'query' in event:
        if event['query'].startswith('update'):
            return execute_update(event['query'])
        else:
            return execute_read(event['query'])


# Write the details of the API response to the DB
def update_database(batch_id, data_1, data_2, status, status_detail):
    log.debug(f"Running update_database with batch_id: {batch_id} "
              f"data_1: {data_1} "
              f"data_2: {data_2} "
              f"status: {status} "
              f"status_detail: {status_detail}")

    today = datetime.now()
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        postgres_insert_query = "UPDATE \"database\".table set "\
                                "updated_timestamp = %s, "\
                                "status = %s,"\
                                "status_detail = %s "\
                                "where batch_id = %s "\
                                "and data_1 = %s "\
                                "and data_2 = %s"
        parameters = (today, status, status_detail, batch_id, data_1, data_2)
        log.debug(f"The sql looks likes this: {postgres_insert_query}")
        log.debug(f"The parameters look like this: {parameters}")
        cursor.execute(postgres_insert_query, parameters)

        connection.commit()
        count = cursor.rowcount
        log.debug(f"{count} rows affected - batch_id:{batch_id} data_1:{data_1} data_2:{data_2} - "
                  "record updated successfully into api_log")

    except (Exception, psycopg2.Error) as error:
        log.error(f"batch_id:{batch_id} data_1:{data_1} data_2:{data_2} - failed to insert record "
                  "into api_log table - {error}")
        raise error

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
