import sqlite3
import pandas as pd


class DataHelper:
    def __init__(self):
        pass

    @staticmethod
    def save_to_sqlite(data: pd.DataFrame, sqlite_file_path: str):
        conn = sqlite3.connect(sqlite_file_path)
        data.to_sql("器者", conn, if_exists="replace", index=False)
        conn.close()
        return True
