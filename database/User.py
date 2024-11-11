class User:
    def __init__(self, uname, uid, upassword, is_adm):
        self.uname = uname
        self.uid = uid
        self.upassword = upassword
        self.is_adm = is_adm

    # 插入用户信息
    def insert_user(self, db_connection):
        cursor = db_connection.cursor()
        query = "INSERT INTO user_ (uname, uid, upassword, is_adm) VALUES (%s, %s, %s, %s)"
        values = (self.uname, self.uid, self.upassword, self.is_adm)
        cursor.execute(query, values)
        db_connection.commit()
        cursor.close()

    # 更新用户信息
    def update_user(self, db_connection):
        cursor = db_connection.cursor()
        query = "UPDATE user_ SET uname=%s, upassword=%s, is_adm=%s WHERE uid=%s"
        values = (self.uname, self.upassword, self.is_adm, self.uid)
        cursor.execute(query, values)
        db_connection.commit()
        cursor.close()

    # 获取用户信息
    @staticmethod
    def get_user(db_connection, uid):
        cursor = db_connection.cursor(dictionary=True)
        query = "SELECT * FROM user_ WHERE uid = %s"
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        cursor.close()
        if result:
            return User(result['uname'], result['uid'], result['upassword'], result['is_adm'])
        else:
            return None
