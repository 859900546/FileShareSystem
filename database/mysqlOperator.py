import datetime
import mysql.connector


def create_db_connection():
    return mysql.connector.connect(
        host="localhost",  # 数据库主机
        user="root",  # 数据库用户名
        password="root",  # 数据库密码
        database="FileShareSystem"  # 数据库名称
    )


def get_now_time():
    return str(datetime.datetime.now())[0:19]

# # 创建数据库连接
# db_connection = create_db_connection()
#
# file_ = File.File("test.txt", "text/plain", "123456", 32,"txt",str(datetime.datetime.now()),)
#
# file_.insert_file(db_connection)
