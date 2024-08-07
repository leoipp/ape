import sqlite3
import pandas as pd


class Database:
    def __init__(self, db):
        self.db = db

    def connect(self):
        return sqlite3.connect(self.db)

    def create_table_from_dataframe(self, df, table_name):
        """
        Create a table in the database from a DataFrame.

        :param df: The DataFrame to be written to the table.
        :param table_name: The name of the table to be created.
        """
        try:
            with self.connect() as conn:
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def fetch_all(self, table_name):
        """
        Fetch all data from a table in the database.

        :param table_name: The name of the table to fetch data from.
        :return: DataFrame with the data.
        """
        try:
            with self.connect() as conn:
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                # df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)
                return df
        except Exception as e:
            print(f"An error occurred: {e}")
            return pd.DataFrame()

    def list_tables(self):
        """
        List all tables in the database.
        :return: List of table names.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                return [table[0] for table in tables]
        except Exception as e:
            print(f"An error occurred: {e}")
            return []