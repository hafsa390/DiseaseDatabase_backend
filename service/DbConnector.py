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
        pool_size=3,
        pool_reset_session=True,
        host="us-cluster-east-01.k8s.cleardb.net",
        port=3306,
        user="b21a0d6691d78d",
        password="c769f560",
        database="heroku_cfdf27f94532903",
    )
except Error as e:
    print(e)
    logger.error(e)
    

def get_db_cursor():
    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            return connection
    except Error as err:
        logger.error(err)
        raise




# def get_db_cursor():
#     connection = None

#     while connection is None:
#         try:
#             connection = connection_pool.get_connection()
#         except Error as err:
#             print(err)
#             logger.error(err)

#     return connection, connection.cursor()
