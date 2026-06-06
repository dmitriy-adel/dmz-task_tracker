import os
import psycopg2


private_vars = os.environ

DB_HOST: str = private_vars["DB_HOST"]
DB_PORT: str = private_vars["DB_PORT"]
DB_NAME: str = private_vars["DB_NAME"]
DB_USER: str = private_vars["DB_USER"]
DB_PASSWORD: str = private_vars["DB_PASSWORD"]


class DBConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        self.conn.autocommit = True

    # ============================ USER Requests ============================

    def get_user_by_id(self, user_id: int) -> dict:
        try:
            query = f"""
                SELECT u.name, u.email, u.used_theme, u.email_notifications_enabled, u.created_at
                FROM users as u
                WHERE u.id = {user_id};
            """

            with self.conn.cursor() as cursor:
                cursor.execute(query)
                cursor_fetch = cursor.fetchall()
                res: dict = {"name": cursor_fetch[0][0],
                            "email": cursor_fetch[0][1],
                            "used_theme": cursor_fetch[0][2],
                            "email_notifications_enabled": cursor_fetch[0][3],
                            "created_at": cursor_fetch[0][4]}
                return res
        
        except Exception as _ex:
            print(f"[db_connection.py->get_user_by_id]. Error :: {_ex}")
            raise RuntimeError(status_code=500, detail="DB request error")
        
    def get_user_pswd(self, user_id: int) -> dict:
        try:
            query = f"""
                SELECT u.hashed_pswd
                FROM users as u
                WHERE u.id = {user_id};
            """

            with self.conn.cursor() as cursor:
                cursor.execute(query)
                cursor_fetch = cursor.fetchall()
                res: dict = {"pswd": cursor_fetch[0][0]}
                return res
        
        except Exception as _ex:
            print(f"[db_connection.py->get_user_by_id]. Error :: {_ex}")
            raise RuntimeError(status_code=500, detail="DB request error")
        
    def add_user(self, name: str, email: str, hash_password: str):
        try:
            query = f"""
                INSERT INTO users(name, email, hash_pswd)
                VALUES ('{name}', '{email}', '{hash_password}');
            """

            with self.conn.cursor() as cursor:
                cursor.execute(query)

        except Exception as _ex:
            print(f"[db_connection.py->create_user]. Error :: {_ex}")
            raise RuntimeError(status_code=500, detail="DB request error")    
