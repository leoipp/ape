import sqlite3
import pandas as pd
from PyQt5 import QtSql, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel


class Database:
    def __init__(self, db):
        self.db = db

    def connect(self):
        return sqlite3.connect(self.db)

    def list_apexes(self):
        """
        Lists all tables in the SQLite database.

        :return: A list of table names.
        """
        # Connect to the SQLite database
        with self.connect() as conn:
            try:
                # Create a cursor object
                cur = conn.cursor()
                # Execute the query to list tables
                cur.execute("SELECT name FROM sqlite_master WHERE type='table';")

                # Fetch all results and extract table names
                tables = [table[0] for table in cur.fetchall()]

            except Exception as e:
                # Handle exceptions if necessary
                print(f"An error occurred: {e}")
                tables = []

        # The connection is automatically closed when leaving the 'with' block
        return tables

    def create_table_from_dataframe(self, df, table_name, parent=None):
        """
        Create a table in the database from a DataFrame, including a primary key column.

        :param df: The DataFrame to be written to the table.
        :param table_name: The name of the table to be created.
        :param parent: The parent widget to attach the popup to.
        """
        try:
            # Convert all string elements in the DataFrame to uppercase
            df = df.apply(lambda col: col.map(lambda x: x.upper() if isinstance(x, str) else x))

            # Add a primary key column
            df.insert(0, 'id', range(1, len(df) + 1))

            with self.connect() as conn:
                # Write the DataFrame to a temporary table without a primary key
                temp_table = f"temp_{table_name}"
                df.to_sql(temp_table, conn, if_exists='replace', index=False)

                # Get the column names and types from the DataFrame
                columns = ', '.join([f'"{col}"' for col in df.columns])

                # Create the final table with a primary key
                cursor = conn.cursor()
                cursor.execute(f"""
                    CREATE TABLE {table_name} (
                        id INTEGER PRIMARY KEY,
                        {', '.join([f'"{col}" {dtype}' for col, dtype in zip(df.columns[1:], df.dtypes)])}
                    )
                """)

                # Insert data from the temporary table into the final table
                cursor.execute(f"INSERT INTO {table_name} ({columns}) SELECT {columns} FROM {temp_table}")
                cursor.execute(f"DROP TABLE {temp_table}")
                conn.commit()

                self.show_popup(f"Tabela '{table_name}' criada com sucesso com 'id' como chave primária.",'white', parent)
        except Exception as e:
            self.show_popup(f"Erro: {e}", 'red', parent)

    def fetch_all(self, table_name, parent=None):
        """
        Fetch all data from a table in the database.

        :param parent: The parent widget to attach the popup to.
        :param table_name: The name of the table to fetch data from.
        :return: DataFrame with the data.
        """
        try:
            with self.connect() as conn:
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                df = df.apply(lambda col: col.map(lambda x: x.upper() if isinstance(x, str) else "{:,.2f}".format(x).replace(',', 'X').replace('.', ',').replace('X', '.') if isinstance(x, (int, float)) else x))
                return df
        except Exception as e:
            self.show_popup(f"Erro: {e}", 'red', parent)
            return pd.DataFrame()

    def list_tables(self, parent=None):
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
            self.show_popup(f"Erro: {e}", 'red', parent)
            return []

    def create_table_with_data(self, table_name, headers, data, parent=None):
        """
        Create a table in the database with the specified headers and data.

        :param table_name: The name of the table to be created.
        :param headers: A list of headers (column names) for the table.
        :param data: A list of lists, where each sublist contains the values for each header.
        """
        try:
            if table_name in self.list_tables():
                self.show_popup(f"Tabela '{table_name}' existente. Substituindo dados...", 'white', parent)
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
            self.show_popup(f"Tabela '{table_name}' criada com sucesso.", 'white', parent)
        except Exception as e:
            self.show_popup(f"Erro: {e}", 'red', parent)

    def append_data_to_table(self, table_name, headers, data, parent=None):
        """
        Append data to an existing table in the database with a primary key `id`, or create the table if it does not exist.

        :param table_name: The name of the table to append data to.
        :param headers: A list of headers (column names) for the table.
        :param data: A list of lists, where each sublist contains the values for each header.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # Check if the table exists
                if table_name not in self.list_tables():
                    self.show_popup(f"Tabela '{table_name}' não existe. Criando nova tabela com chave primária 'id'...", 'white',
                                    parent)

                    # Create the table with an auto-incrementing primary key `id`
                    create_table_sql = f"""
                    CREATE TABLE {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        {', '.join([f"{header} TEXT" for header in headers])}
                    )
                    """
                    cursor.execute(create_table_sql)
                    conn.commit()

                # Ensure that the length of each row in data matches the number of headers
                if not all(len(row) == len(headers) for row in data):
                    raise ValueError("Each row of data must match the number of headers.")

                # Prepare the SQL insert statement
                placeholders = ', '.join(['?' for _ in headers])
                insert_sql = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"

                # Insert data into the table
                cursor.executemany(insert_sql, data)
                conn.commit()

                self.show_popup(f"Dados adicionados à tabela '{table_name}' com sucesso.", 'white', parent)
        except Exception as e:
            self.show_popup(f"Erro ao adicionar dados à tabela '{table_name}': {e}", 'red', parent)

    def drop_table(self, table_name, parent=None):
        """
        Drop a table from the database if it exists.

        :param table_name: The name of the table to drop.
        :param parent: Parent widget for displaying messages (optional).
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                conn.commit()
                self.show_popup(f"Tabela '{table_name}' foi removida com sucesso.", 'white', parent)
        except Exception as e:
            self.show_popup(f"Erro: {e}", 'red', parent)

    def create_tabs_for_apex_manejo_tables(self, add_new_tab_method):
        """
        Create tabs for all tables matching the 'Apex_Manejo%' pattern.

        :param add_new_tab_method: The method to add new tabs, usually passed as self.add_new_tab.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Apex_Manejo%';")
                tables = cursor.fetchall()

                for table in tables:
                    table_name = table[0]
                    add_new_tab_method(table_name)

        except sqlite3.Error as e:
            print(f"An error occurred while querying the database: {e}")

    def populate_tree_with_tables_and_columns(self, tree_widget):
        """
        Populates a QTreeWidget with tables and columns from the SQLite database.
        :param tree_widget: The QTreeWidget to populate.
        """
        with self.connect() as conn:
            cur = conn.cursor()

            tree_widget.clear()  # Clear previous items

            # Query to get the list of tables
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()

            for table in tables:
                table_name = table[0]
                table_item = QtWidgets.QTreeWidgetItem(tree_widget, [table_name])
                table_item.setExpanded(False)  # Ensure the table item is not expanded

                # Query to get columns for the current table
                cur.execute(f"PRAGMA table_info({table_name});")
                columns = cur.fetchall()

                for column in columns:
                    column_name = column[1]
                    QtWidgets.QTreeWidgetItem(table_item, [column_name])

    def execute_query_db(self, query_text):
        """
        Executes an SQL query and returns the results.

        :param query_text: The SQL query to execute.
        :return: A tuple containing column headers and rows of results.
        """
        try:
            with self.connect() as conn:
                cur = conn.cursor()

                # Execute the query
                cur.execute(query_text)
                results = cur.fetchall()

                # Get the column headers
                headers = [description[0] for description in cur.description]

                return headers, results

        except sqlite3.Error as e:
            msg = QtWidgets.QMessageBox()
            msg.setText(f'Não foi possível executar a query.\nErro: {e}')
            msg.setWindowTitle("Erro ao executar query")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return None, None

    @staticmethod
    def show_popup(message, color='white', parent=None):
        popup = QLabel(message, parent)
        popup.setStyleSheet(f"""
                    QLabel {{
                        background-color: rgba(135, 134, 114, 0.45);
                        color: {color};
                        font-family: 'Poppins';
                        font-size: 8pt;  
                        padding: 10px;
                        border: 1px solid rgba(135, 134, 114, 0.45);
                        border-radius: 10px;
                    }}
                """)
        popup.setWindowFlags(Qt.FramelessWindowHint)
        popup.setAlignment(Qt.AlignCenter)

        # Position the popup at the bottom center of the parent widget
        if parent:
            popup.setGeometry(parent.width() // 2 - 250, parent.height() - 100, 500, 50)
        else:
            # Fallback position if no parent is provided
            popup.setGeometry(100, 100, 500, 50)

        popup.show()

        # Timer to close the popup after 10 seconds
        QTimer.singleShot(15000, popup.close)
