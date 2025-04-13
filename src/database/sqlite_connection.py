import sqlite3
#这个类后续要扩展成sqlite数据源的类

class SqliteConnector:

    db_type: str = "sqlite"
    db_dialect: str = "sqlite"
    def __init__(self,db_file_path):
        self.db_file_path = db_file_path if db_file_path is not None else "chinook.db"
        self.conn = sqlite3.connect(self.db_file_path)
        self.cursor = self.conn.cursor()

    def execute_sql(self,sql):
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        return columns,rows

    #最基础的信息：表(字段)
    def get_table_simple_info(self):
        columns,table_infos = self.execute_sql("SELECT name FROM sqlite_master WHERE type = 'table'")
        tables = [table_info[0] for table_info in table_infos]
        results = []
        for table in tables:
            print(table)
            data_columns,columns = self.execute_sql(f"PRAGMA table_info({table})")
            table_columns = []
            print(columns)
            for row_column in columns:
                field_info = list(row_column)
                table_columns.append(field_info[1])

            results.append(f"{table}({','.join(table_columns)})")

        return results

    def close_connection(self):
        self.conn.close()