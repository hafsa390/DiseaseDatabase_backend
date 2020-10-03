import mysql.connector
import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import logging as logger

try:
    # Dev config
    # connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    #     pool_name="hma_pool",
    #     pool_size=20,
    #     pool_reset_session=True,
    #     host="localhost",
    #     port=3306,
    #     user="root",
    #     password="1234567890",
    #     database="HMA",
    # )

    # Prod config
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="hma_pool",
        pool_size=20,
        pool_reset_session=True,
        host="127.0.0.1",
        port=3306,
        user="root",
        password="Avengers1234567890!!!",
        database="HMA",
    )
except Error as e:
    print(e)
    logger.error(e)


def get_db_cursor():
    connection = None

    while connection is None:
        try:
            connection = connection_pool.get_connection()
        except Error as err:
            print(err)
            logger.error(err)

    return connection, connection.cursor()
