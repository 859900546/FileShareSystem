import datetime
import mysql.connector
from config.config import settings


def create_db_connection():
    return mysql.connector.connect(
        host=settings.MYSQL_HOST,  # 数据库主机
        user=settings.MYSQL_USERNAME,  # 数据库用户名
        password=settings.MYSQL_PASSWORD,  # 数据库密码
        database=settings.MYSQL_DATABASE  # 数据库名称
    )


def get_now_time():
    return str(datetime.datetime.now())[0:19]

# # 创建数据库连接
# db_connection = create_db_connection()
#
# file_ = File.File("test.txt", "text/plain", "123456", 32,"txt",str(datetime.datetime.now()),)
#
# file_.insert_file(db_connection)
