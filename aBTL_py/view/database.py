import pymysql

class Database:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="btlpy"
            )
            self.cursor = self.conn.cursor()
        except pymysql.MySQLError as e:
            print(f" Lỗi kết nối MySQL: {e}")

    def ket_noi(self, query, values=None):
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            if query.strip().lower().startswith("select"):
                return self.cursor.fetchall()
            return True
        except Exception as e:
            print(f" Lỗi truy vấn SQL: {e}")
            return None

    def dong_ket_noi(self):
        self.cursor.close()
        self.conn.close()
