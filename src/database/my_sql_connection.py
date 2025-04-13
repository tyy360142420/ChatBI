import mysql.connector



class MySqlConnection:

    db_type: str = "mysql"
    db_dialect: str = "mysql"
    def __init__(self,host,user,password,database):
        self.host = host
        self.database = database
        self.mysql_conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.mysql_conn.cursor()

    def execute_sql(self,sql):
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        return columns,rows

    def get_table_simple_infos(self):
        sql_for_get_tables = """
                show tables
            """
        result_of_query_tables = self.execute_sql(sql_for_get_tables)
        table_result = []
        for row in result_of_query_tables:
            table_name = row[0]
            sql_for_get_table_column_info = f"""
                SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE
                 TABLE_NAME='{table_name}'
            """
            result_of_query_columns = self.execute_sql(sql_for_get_table_column_info)
            table_columns = []
            for column in result_of_query_columns:
                field_info = list(column)
                table_columns.append(field_info[0])
            table_result.append(f"{table_name}({','.join(table_columns)});")
        return table_result



    def close_connection(self):
        self.mysql_conn.close()