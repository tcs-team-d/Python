import os
import logging
import psycopg2



def get_db_connection():
    try:
        conn = psycopg2.connect(
            # host=os.environ['DB_HOST'],
            # user=os.environ['DB_USER'],
            # password=os.environ['DB_PASSWORD'],
            # dbname=os.environ['DB_NAME'],
            host='hopcast.postgres.database.azure.com',
            user='hopcast',
            password='Hc1234567',
            dbname='postgres',
            sslmode='require',
            options='-c timezone=Asia/Tokyo'
        )
        return conn
    except psycopg2.Error as e:
        logging.error(e)
        raise


def insert_weather_record(conn, data: dict):
    column_map = {
        'time': 'record_date',
    }
    columns = [column_map.get(k, k) for k in data.keys()]
    values = [data[k][0] for k in data.keys()]

    columns_str = ','.join(columns) # type: ignore
    placeholders = ','.join(['%s'] * len(values))

    sql = f"""
        INSERT INTO
            weather_records (
                {columns_str}
            ) 
            VALUES (
                {placeholders}
            )
    """
    with conn.cursor() as cur:
        cur.execute(sql, values)
    conn.commit()