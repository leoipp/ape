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
                df = df.apply(lambda col: col.map(lambda x: x.upper() if isinstance(x, str) else "{:,.2f}".format(x).replace(',', 'X').replace('.', ',').replace('X', '.') if isinstance(x, (int, float)) else x))
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

    def create_table_with_data(self, table_name, headers, data):
        """
        Create a table in the database with the specified headers and data.

        :param table_name: The name of the table to be created.
        :param headers: A list of headers (column names) for the table.
        :param data: A list of lists, where each sublist contains the values for each header.
        """
        try:
            if table_name in self.list_tables():
                print(f"Table '{table_name}' already exists. Replacing data...")
                # Option 1: Drop the existing table and create a new one
                with self.connect() as conn:
                    conn.execute(f"DROP TABLE IF EXISTS {table_name}")

                # Option 2: Delete all rows from the existing table (keeping the structure)
                # with self.connect() as conn:
                #     conn.execute(f"DELETE FROM {table_name}")

            # Ensure that the length of each row in data matches the number of headers
            if not all(len(row) == len(headers) for row in data):
                raise ValueError("Each row of data must match the number of headers.")

            # Create a DataFrame from the headers and data
            df = pd.DataFrame(data, columns=headers)

            # Create the table from the DataFrame
            self.create_table_from_dataframe(df, table_name)
            print(f"Table '{table_name}' with provided data created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the table: {e}")