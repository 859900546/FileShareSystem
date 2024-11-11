import mysql.connector
from . import User, File


def create_db_connection():
    return mysql.connector.connect(
        host="localhost",  # 数据库主机
        user="root",  # 数据库用户名
        password="root",  # 数据库密码
        database="FileShareSystem"  # 数据库名称
    )


# 创建数据库连接
db_connection = create_db_connection()

