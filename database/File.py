class File:
    def __init__(self, fname, fpath, uid, fsize, ftype, fdate, findex):
        self.fname = fname
        self.fpath = fpath
        self.uid = uid
        self.fsize = fsize
        self.ftype = ftype
        self.fdate = fdate
        self.findex = findex

    # 插入文件信息
    def insert_file(self, db_connection):
        cursor = db_connection.cursor()
        query = "INSERT INTO file_ (fname, fpath, uid, fsize, ftype, fdate, findex) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.fname, self.fpath, self.uid, self.fsize, self.ftype, self.fdate, self.findex)
        cursor.execute(query, values)
        db_connection.commit()
        cursor.close()

    # 更新文件信息
    def update_file(self, db_connection):
        cursor = db_connection.cursor()
        query = "UPDATE file_ SET fname=%s, fpath=%s, fsize=%s, ftype=%s, fdate=%s, findex=%s WHERE uid=%s AND fname=%s"
        values = (self.fname, self.fpath, self.fsize, self.ftype, self.fdate, self.findex, self.uid, self.fname)
        cursor.execute(query, values)
        db_connection.commit()
        cursor.close()

    # 获取文件信息
    @staticmethod
    def get_file_by_user(db_connection, uid):
        cursor = db_connection.cursor(dictionary=True)
        query = "SELECT * FROM file_ WHERE uid = %s"
        cursor.execute(query, (uid,))
        result = cursor.fetchall()
        cursor.close()
        files = []
        for row in result:
            file_obj = File(row['fname'], row['fpath'], row['uid'], row['fsize'], row['ftype'], row['fdate'], row['findex'])
            files.append(file_obj)
        return files
