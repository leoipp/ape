import sqlite3
import pandas as pd
import statistics


class Consist:
    def __init__(self, db):
        self.db = db
        self.temp_table_counter = 0

    def connect(self):
        return sqlite3.connect(self.db)

    def vacuum_database(self):
        """
        Perform a VACUUM operation on the SQLite database.

        The VACUUM command rebuilds the database file, compacts it, and reclaims unused space.
        This operation can significantly reduce the size of the database file, particularly
        if a large amount of data has been deleted. It also helps to defragment the database,
        potentially improving query performance.

        The VACUUM operation locks the entire database, so it is recommended to run this
        function during a maintenance window when the database is not heavily used.

        Raises:
        -------
        sqlite3.Error
            If an error occurs during the VACUUM operation, it will be caught and displayed.

        Example:
        --------
        db_manager = DatabaseManager('your_database.db')
        db_manager.vacuum_database()
        """
        try:
            with self.connect() as conn:
                cur = conn.cursor()
                cur.execute("VACUUM")
                conn.commit()
                print("Database vacuumed successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred during the VACUUM operation: {e}")

    def list_tables(self):
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

    def fetch_row_by_rowid(self, table_name, rowid):
        """
        Fetch the values of a row from a table based on the rowid.

        :param table_name: The name of the table to fetch the row from.
        :param rowid: The rowid of the row to fetch.
        :return: A dictionary with column names as keys and the corresponding row values as values.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # Fetch column names
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = [column[1] for column in cursor.fetchall()]

                # Fetch the row based on the rowid
                cursor.execute(f"SELECT * FROM {table_name} WHERE rowid = ?", (rowid,))
                row_values = cursor.fetchone()

                if row_values:
                    # Create a dictionary of column names and row values
                    result = dict(zip(columns, row_values))
                    return result
                else:
                    print(f"No row found with rowid {rowid} in table '{table_name}'.")
                    return None

        except sqlite3.Error as e:
            print(f"An error occurred while fetching the row: {e}")
            return None

    def add_column(self, table_name, column_name, data_type="FLOAT"):
        """
        Ensures the specified column exists in the table; creates it if not.

        :param table_name: Name of the table.
        :param column_name: Name of the column to check or create.
        :param data_type: Data type of the column if it needs to be created. Default is "FLOAT".
        """
        with self.connect() as conn:
            cur = conn.cursor()

            # Check if the column already exists in the table
            cur.execute(f"PRAGMA table_info({table_name})")
            existing_columns = [column[1] for column in cur.fetchall()]

            # Add the column if it doesn't exist
            if column_name not in existing_columns:
                cur.execute(f"""
                    ALTER TABLE {table_name}
                    ADD COLUMN {column_name} {data_type}
                """)

    def regional_resumo(self, table_name, regime, other, n, coluna="Area"):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(
                f"""
                SELECT {coluna}
                FROM {table_name}
                WHERE ManejoAPEX_Final = '{regime}' AND SUBSTR(Talhao, {n}, 2) = '{other}'
                """
            )
            r = cur.fetchall()
            r = [a[0] for a in r if a[0] is not None]
            sum_r = round(sum(r))
            return sum_r

    def regional_resumo_av(self, table_name, regime, other, n, coluna="Area", soma='True'):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(
                f"""
                SELECT {coluna}
                FROM {table_name}
                WHERE ManejoAPEX_Final = '{regime}' AND SUBSTR(Talhao, {n}, 2) = '{other}'
                """
            )
            r = cur.fetchall()
            r = [a[0] for a in r if a[0] is not None]
            if soma == 'True':
                sum_r = round(sum(r))
                return sum_r
            else:
                try:
                    mean_r = round(sum(r)/len(r))
                except Exception:
                    mean_r = 0
                print(mean_r)
                return mean_r

    def fetch_all_data(self, table_name):
        """
        Fetch all rows from the specified table.

        :param table_name: The name of the table to fetch data from.
        :return: A DataFrame containing all rows from the table.
        """
        with self.connect() as conn:
            cur = conn.cursor()
            query = f"SELECT * FROM {table_name}"
            cur.execute(query)
            rows = cur.fetchall()

            # Get column names
            columns = [desc[0] for desc in cur.description]

            # Convert to DataFrame
            df = pd.DataFrame(rows, columns=columns)

        return df

    def update_table(self, table_name: str, col_calc: dict):
        """
        Updates the table with calculated values for specific columns.

        :param table_name: Name of the table to update.
        :param col_calc: Dictionary where the key is the column name and the value is a tuple of (calculation, data type).
        """
        # Ensure all required columns exist
        for column_name, (calculation, data_type) in col_calc.items():
            self.add_column(table_name, column_name, data_type)

        # Perform the update calculations
        with self.connect() as conn:
            cur = conn.cursor()
            for column_name, (calculation, data_type) in col_calc.items():
                cur.execute(f"""
                    UPDATE {table_name}
                    SET {column_name} = {calculation}
                """)

    def aggregate_data(self, group_by_column, table_suffix, output_columns):
        """
        Creates an aggregated table based on the specified grouping column.

        :param group_by_column: The column to group by (e.g., 'lote', 'projeto', 'chave_sub_reg').
        :param table_suffix: The suffix for the new table name (e.g., 'lote', 'projeto', 'sub_regiao').
        :param output_columns: A dictionary mapping the original columns to their new aggregated names.
        """
        table_name = f"IFC_{table_suffix}"

        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("BEGIN;")

            # Construct the SQL query dynamically
            aggregation_clauses = [
                f"SUM({original})/SUM(area) AS {agg_name}"
                for original, agg_name in output_columns.items()
            ]
            aggregation_clauses.append("DATE(ROUND(AVG(julianday(DT_Medicao)), 0)) AS AGGDT")
            aggregation_sql = ", ".join(aggregation_clauses)

            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} AS
                SELECT
                    {group_by_column},
                    {aggregation_sql}
                FROM
                    IFC
                GROUP BY
                    {group_by_column}
            """

            cur.execute(query)
            cur.execute("COMMIT;")
            print(f"Table '{table_name}' created successfully.")

    def create_temp_table(self, base_table, join_table, columns, join_column, old_join_column, ref_column):
        """
        Creates a temporary table by joining the base table with another table,
        using COALESCE to handle null values.

        :param base_table: The main table to join.
        :param join_table: The table to join with the base table.
        :param columns: List of columns to include from the join table.
        :param join_column: The column in the base table to join on.
        :param old_join_column: An alternative column in the base table to join on if the first join fails.
        :param ref_column: The reference column in the join table.
        """
        with self.connect() as conn:
            cur = conn.cursor()

            # Prepare COALESCE clauses for each column to handle null values
            coalesce_columns = [
                f"COALESCE(i.{col}, i2.{col}) AS {col}_{join_table}"
                for col in columns
            ]
            coalesce_clause = ", ".join(coalesce_columns)

            # Generate a unique temporary table name
            self.temp_table_counter += 1
            temp_table_name = f"Apex_temp_{self.temp_table_counter}"

            # Create the SQL query for the temporary table
            query = f"""
                CREATE TABLE IF NOT EXISTS {temp_table_name} AS
                SELECT
                    t.*,
                    {coalesce_clause}
                FROM
                    {base_table} t
                LEFT JOIN
                    {join_table} i ON t.{join_column} = i.{ref_column}
                LEFT JOIN
                    {join_table} i2 ON t.{old_join_column} = i2.{ref_column} AND i.{ref_column} IS NULL
            """

            cur.execute(query)
            print(f"Temporary table '{temp_table_name}' created successfully.")

    @staticmethod
    def update_table_with_values(conn, target_table, source_table, source_columns, join_column, target_columns):
        """
        Updates the target table with values from the source table based on a join column,
        only if the current value in the target table is NULL.

        :param conn: The active SQLite connection to use.
        :param target_table: The name of the target table to update.
        :param source_table: The name of the source table providing the data.
        :param source_columns: A list of columns from the source table to use in the update.
        :param join_column: The column used to join the target and source tables.
        :param target_columns: A list of columns in the target table to update.
        """
        cur = conn.cursor()

        update_clauses = [
            f"{target_col} = CASE WHEN {target_table}.{target_col} IS NULL THEN {source_table}.{source_col} ELSE {target_table}.{target_col} END"
            for target_col, source_col in zip(target_columns, source_columns)
        ]
        update_clause = ", ".join(update_clauses)

        query = f"""
            UPDATE {target_table}
            SET {update_clause}
            FROM {source_table}
            WHERE {target_table}.{join_column} = {source_table}.{join_column}
        """

        cur.execute(query)
        print(f"Table '{target_table}' updated with data from '{source_table}'.")

    def create_and_populate_final_table(self):
        """
        Creates the final table and populates it with data from various temporary tables.

        The process involves:
        1. Creating the 'apex_base_0' table if it doesn't exist.
        2. Inserting initial data from 'apex_temp_1'.
        3. Populating the final table with data from other temporary tables, prioritizing the data source.
        """
        with self.connect() as conn:
            cur = conn.cursor()

            cur.execute("DROP TABLE IF EXISTS apex_base_0")
            # Step 1: Create the final table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS apex_base_0 (
                    TalhaoAtual TEXT,
                    VTCC FLOAT,
                    Fustes INTEGER,
                    DT_Medicao TEXT
                )
            """)

            # Step 2: Insert initial data from apex_tmp_1
            cur.execute("""
                INSERT INTO apex_base_0 (TalhaoAtual, VTCC, Fustes, DT_Medicao)
                SELECT TalhaoAtual, VTCC_IFPC, Fustes_IFPC, DT_Medicao_IFPC FROM Apex_temp_1
            """)

            # Step 3: Define the mapping of source tables and columns
            table_column_mapping = {
                'apex_temp_2': ['VTCC_IFC', 'Fustes_IFC', 'DT_Medicao_IFC'],
                'apex_temp_3': ['AGGL_VTCC_IFC_Lote', 'AGGL_Fustes_IFC_Lote', 'AGGDT_IFC_Lote'],
                'apex_temp_4': ['AGGP_VTCC_IFC_Projeto', 'AGGP_Fustes_IFC_Projeto', 'AGGDT_IFC_Projeto'],
                'apex_temp_5': ['AGGSR_VTCC_IFC_SubRegiao', 'AGGSR_Fustes_IFC_SubRegiao','AGGDT_IFC_SubRegiao']
            }

            # Step 4: Define the target columns in the final table
            target_columns = ['VTCC', 'Fustes', 'DT_Medicao']

            # Step 5: Populate the final table with data from the other temp tables
            for table, source_columns in table_column_mapping.items():
                self.update_table_with_values(conn, 'apex_base_0', table, source_columns, 'TalhaoAtual', target_columns)

        print("Final table 'apex_base_0' created and populated successfully.")

    def create_final_table_2(self):
        """
        Creates and populates the 'apex_base_1' table, then updates it with data from other tables.

        Steps:
        1. Create 'apex_base_1' table if it doesn't exist.
        2. Insert initial data from 'apex_base_0'.
        3. Update 'apex_base_1' with data from 'apex_tmp_6'.
        4. Calculate and update 'idade' and 'idade_classe' fields.
        """
        with self.connect() as conn:
            cur = conn.cursor()

            # Step 1: Create the final table 'apex_base_1' if it doesn't exist
            self._create_apex_base_1_table(cur)

            # Step 2: Insert initial data from 'apex_base_0'
            self._insert_initial_data(cur)

            # Step 3: Update 'apex_base_1' with data from 'apex_tmp_6'
            self._update_with_apex_tmp_6(cur)

            # Step 4: Calculate and update 'idade' and 'idade_classe'
            self._calculate_and_update_idade(cur)

            print("Final table 'apex_base_1' created and populated successfully.")

    @staticmethod
    def _create_apex_base_1_table(cur):
        """
        Creates the 'apex_base_1' table structure.

        :param cur: SQLite cursor to execute the query.
        """
        cur.execute("DROP TABLE IF EXISTS apex_base_1")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS apex_base_1 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                DCR_Projeto TEXT,
                Regiao TEXT,
                Talhao TEXT,
                Regime TEXT,
                Area FLOAT,
                DT_Plantio TEXT,
                DT_Medicao TEXT,
                Idade FLOAT,
                IdadeClasse FLOAT,
                ESP TEXT,
                DCR_MatGen TEXT,
                VTCC FLOAT,
                Fustes INTEGER,
                DIST_LP FLOAT,
                DIST_PFRod FLOAT,
                DIST_PFFer FLOAT,
                DIST_LFRod FLOAT,
                DIST_Total FLOAT
            )
        """)

    @staticmethod
    def _insert_initial_data(cur):
        """
        Inserts initial data into 'apex_base_1' from 'apex_base_0'.

        :param cur: SQLite cursor to execute the query.
        """
        cur.execute("""
            INSERT INTO apex_base_1 (Talhao, VTCC, Fustes, DT_Medicao, Regiao, Regime)
            SELECT TalhaoAtual, VTCC, Fustes, DT_Medicao, 
                   SUBSTR(TalhaoAtual, 3, 2) AS Regiao, 
                   SUBSTR(TalhaoAtual, 12, 1) AS Regime
            FROM apex_base_0
        """)

    @staticmethod
    def _update_with_apex_tmp_6(cur):
        """
        Updates 'apex_base_1' with data from 'apex_tmp_6'.

        :param cur: SQLite cursor to execute the query.
        """
        update_columns = {
            'DCR_Projeto': 'DCR_Projeto_CadastroFlorestal',
            'Area': 'Area_CadastroFlorestal',
            'DCR_MatGen': 'DCR_MatGen_CadastroFlorestal',
            'ESP': 'ESP_CadastroFlorestal',
            'DT_Plantio': 'DT_Plantio_CadastroFlorestal',
            'DIST_LP': 'DIST_LP_CadastroFlorestal',
            'DIST_PFRod': 'DIST_PFRod_CadastroFlorestal',
            'DIST_PFFer': 'DIST_PFFer_CadastroFlorestal',
            'DIST_LFRod': 'DIST_LFRod_CadastroFlorestal',
            'DIST_Total': 'DIST_Total_CadastroFlorestal'
        }

        for target_col, source_col in update_columns.items():
            cur.execute(f"""
                UPDATE apex_base_1
                SET {target_col} = (
                    SELECT {source_col} FROM apex_temp_6
                    WHERE apex_temp_6.TalhaoAtual = apex_base_1.Talhao
                )
                WHERE {target_col} IS NULL
            """)

    @staticmethod
    def _calculate_and_update_idade(cur):
        """
        Calculates and updates 'idade' and 'idade_classe' in 'apex_base_1'.

        :param cur: SQLite cursor to execute the queries.
        """
        cur.execute("""
            UPDATE apex_base_1
            SET Idade = (
                SELECT CAST((JULIANDAY(DT_Medicao) - JULIANDAY(DT_Plantio)) / 365.25 AS FLOAT)
            )
            WHERE DT_Medicao IS NOT NULL AND DT_Plantio IS NOT NULL
        """)

        cur.execute("""
                UPDATE apex_base_1
                SET IdadeClasse = CASE
                    WHEN Idade - FLOOR(Idade) < 0.25 THEN FLOOR(Idade)
                    WHEN Idade - FLOOR(Idade) >= 0.25 AND Idade - FLOOR(Idade) < 0.75 THEN FLOOR(Idade) + 0.5
                    ELSE FLOOR(Idade) + 1
                END
                WHERE Idade IS NOT NULL
            """)

    def ajuste_base(self):
        """
        Retrieves records from 'apex_base_1' that need adjustment based on various conditions.

        :return: A tuple containing the rows and their corresponding headers.
        """
        with self.connect() as conn:
            cur = conn.cursor()

            # Step 1: Execute the query to select rows needing adjustment
            rows = self._select_adjustment_rows(cur)

            # Step 2: Retrieve headers from the cursor description
            headers = self._get_headers_from_cursor(cur)

            df = pd.DataFrame(rows, columns=headers)
            # Step 3: Close the cursor and return the results
            cur.close()

            return df

    def print_ajuste_base(self, table_name):
        """
        Consolidates data by counting records in the specified table that meet certain conditions.

        :param table_name: Name of the table to consolidate.
        :return: A list of counts for various conditions.
        """
        conditions = {
            'null_count_matgen': "DCR_MatGen IS NULL OR DCR_MatGen = 'None' OR DCR_MatGen = 0",
            'null_count_dist': "DIST_Total IS NULL OR DIST_Total = 'None'",
            'null_count_esp': "ESP IS NULL OR ESP = 'None'",
            'count_esp_ind': "ESP = 'Indefinido'",
            'null_count_id': "Idade IS NULL OR Idade = 0",
            'count_id_neg': "Idade < 0",
            'null_count_area': "Area IS NULL OR Area = 'None' OR Area = 0",
            'null_count_prod': "VTCC IS NULL OR VTCC = 'None' OR VTCC = 0",
            'count_vtcc_100': "VTCC <= 100",
            'count_vtcc_600': "VTCC >= 600"
        }

        results = []

        with self.connect() as conn:
            cur = conn.cursor()

            for label, condition in conditions.items():
                cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {condition}")
                result = cur.fetchone()
                count = result[0] if result else 0
                results.append(count)

        return results

    @staticmethod
    def _select_adjustment_rows(cur):
        """
        Executes a query to select rows from 'apex_base_1' that require adjustments.

        :param cur: SQLite cursor to execute the query.
        :return: A list of rows that meet the adjustment criteria.
        """
        query = """
            SELECT
                id,
                Talhao,
                Area,
                DCR_MatGen,
                ESP,
                VTCC,
                DT_Plantio,
                DT_Medicao,
                Idade,
                DIST_LP,
                DIST_PFRod,
                DIST_PFFer,
                DIST_LFRod,
                DIST_Total
            FROM apex_base_1
            WHERE
                DCR_MatGen IS NULL OR
                DCR_MatGen = 'None' OR
                DCR_MatGen = 0 OR
                DIST_Total IS NULL OR
                DIST_Total = 'None' OR
                ESP IS NULL OR
                ESP = 'None' OR
                ESP = 'Indefinido' OR
                Idade IS NULL OR
                Idade < 0 OR
                VTCC <= 100 OR
                VTCC >= 600 OR
                Area is NULL OR
                Area = 'None'
        """
        cur.execute(query)
        return cur.fetchall()

    @staticmethod
    def _get_headers_from_cursor(cur):
        """
        Retrieves the column headers from the cursor's description.

        :param cur: SQLite cursor to get the description.
        :return: A list of headers corresponding to the columns selected.
        """
        return [description[0] for description in cur.description]

    def save_changes_to_database(self, table_name, row_data, primary_key_column, table_widget):
        """
        Save the changes for a single row to the database.

        :param table_name: The name of the table in the database.
        :param row_data: A list containing the new row data, including the primary key as the last item.
        :param primary_key_column: The name of the primary key column in the table.
        :param table_widget: The QTableWidget containing the data.
        """
        # Extract the primary key value (last item in row_data)
        row_data = row_data[:-1]
        primary_key_value = row_data[0]
        row_data = row_data[1:]  # Exclude the primary key from the data to be updated

        # Get column names from the table widget
        headers = [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]

        # Exclude the primary key column from the column names
        column_names = headers[1:] if headers[0] == primary_key_column else headers

        # Build the SET clause of the SQL UPDATE query dynamically
        set_clause = ", ".join([f"{col} = ?" for col in column_names])

        # Prepare the SQL UPDATE query
        update_query = f"""
            UPDATE {table_name}
            SET {set_clause}
            WHERE {primary_key_column} = ?
        """

        # Execute the query with the data
        with self.connect() as conn:
            cur = conn.cursor()
            try:
                cur.execute(update_query, (*row_data, primary_key_value))
                conn.commit()
                print(f"Row with primary key {primary_key_value} updated successfully.")
            except sqlite3.Error as e:
                print(f"SQLite error occurred: {e}")

    def delete_selected_rows(self, table_name, table_widget, primary_key_column):
        """
        Delete selected rows from the database and the QTableWidget.

        :param table_name: The name of the table in the database.
        :param table_widget: The QTableWidget containing the data.
        :param primary_key_column: The name of the primary key column in the table.
        """
        selected_rows = table_widget.selectionModel().selectedRows()

        if not selected_rows:
            print("No rows selected for deletion.")
            return

        # Prepare to delete from database
        primary_keys_to_delete = []
        for row in selected_rows:
            primary_key_value = table_widget.item(row.row(), 0).text()  # Assuming primary key is in the first column
            primary_keys_to_delete.append(primary_key_value)

        # Delete from the database
        placeholders = ', '.join('?' for _ in primary_keys_to_delete)
        delete_query = f"DELETE FROM {table_name} WHERE {primary_key_column} IN ({placeholders})"

        with self.connect() as conn:
            cur = conn.cursor()
            try:
                cur.execute(delete_query, primary_keys_to_delete)
                conn.commit()
                print(f"Rows with primary keys {primary_keys_to_delete} deleted successfully.")
            except sqlite3.Error as e:
                print(f"SQLite error occurred: {e}")
                return

        # Remove the rows from the table widget
        for row in sorted(selected_rows, reverse=True):
            table_widget.removeRow(row.row())

    def pipeline(self):
        self.update_table(
            'IFPC',
            {'Projeto': ('SUBSTR(talhao, 1, 11)', 'TEXT'),
             'SubRegiao': ('SUBSTR(Talhao, 5, 2)', 'TEXT'),
             'Regiao': ('SUBSTR(Talhao, 3, 2)', 'TEXT')
             }
        )
        self.update_table('IFC',
                          {'Projeto': ('SUBSTR(talhao, 1, 11)', 'TEXT'),
                           'SubRegiao': ('SUBSTR(Talhao, 5, 2)', 'TEXT'),
                           'Regiao': ('SUBSTR(Talhao, 3, 2)', 'TEXT'),
                           'Lote': ('SUBSTR(Talhao, 1, 14)', 'TEXT'),
                           'Rotacao': ("CASE WHEN SUBSTR(Talhao, 12, 1) = 'R' THEN '1' ELSE '2' END;", 'INTEGER'),
                           'ChaveSubRot': ('SubRegiao||Rotacao', 'TEXT'),
                           'FustesPond': ('Fustes*Area', 'INTEGER'),
                           'VTCCPond': ('VTCC*Area', 'FLOAT'),
                           }
                          )
        self.update_table('Orcamento',
                          {'Projeto': ('SUBSTR(TalhaoAtual, 1, 11)', 'TEXT'),
                           'SubRegiao': ('SUBSTR(TalhaoAtual, 5, 2)', 'TEXT'),
                           'Regiao': ('SUBSTR(TalhaoAtual, 3, 2)', 'TEXT'),
                           'LoteAtual': ('SUBSTR(TalhaoAtual, 1, 14)', 'TEXT'),
                           'LoteAntigo': ('SUBSTR(TalhaoReferencia, 1, 14)', 'TEXT'),
                           'Rotacao': ("CASE WHEN SUBSTR(TalhaoAtual, 12, 1) = 'R' THEN '1' ELSE '2' END;", 'INTEGER'),
                           'ChaveSubRot': ('SubRegiao||Rotacao', 'TEXT')
                           }
                          )
        self.update_table('ClassesInclinacao',
                          {'Pond0_28': ('Area*PCT0_28', 'FLOAT'),
                           'Pond29_Mais': ('Area*(PCT29_38+PCT38_MAIS)', 'FLOAT')
                           }
                          )
        # Aggregating by 'lote'
        self.aggregate_data(
            group_by_column='Lote',
            table_suffix='Lote',
            output_columns={
                'FustesPond': 'AGGL_Fustes',
                'VTCCPond': 'AGGL_VTCC'
            }
        )

        # Aggregating by 'projeto'
        self.aggregate_data(
            group_by_column='Projeto',
            table_suffix='Projeto',
            output_columns={
                'FustesPond': 'AGGP_Fustes',
                'VTCCPond': 'AGGP_VTCC'
            }
        )

        # Aggregating by 'chave_sub_reg'
        self.aggregate_data(
            group_by_column='ChaveSubRot',
            table_suffix='SubRegiao',
            output_columns={
                'FustesPond': 'AGGSR_Fustes',
                'VTCCPond': 'AGGSR_VTCC'
            }
        )

        # Define the parameters for each temp table creation in a list of dictionaries
        temp_table_configs = [
            {
                'base_table': 'Orcamento',
                'join_table': 'IFPC',
                'columns': ['Talhao', 'DT_Medicao', 'Area', 'VTCC', 'Fustes'],
                'join_column': 'TalhaoAtual',
                'old_join_column': 'TalhaoReferencia',
                'ref_column': 'Talhao'
            },
            {
                'base_table': 'Orcamento',
                'join_table': 'IFC',
                'columns': ['Talhao', 'DT_Medicao', 'Area', 'VTCC', 'Fustes'],
                'join_column': 'TalhaoAtual',
                'old_join_column': 'TalhaoReferencia',
                'ref_column': 'Talhao'
            },
            {
                'base_table': 'Orcamento',
                'join_table': 'IFC_Lote',
                'columns': ['Lote', 'AGGL_Fustes', 'AGGL_VTCC', 'AGGDT'],
                'join_column': 'LoteAtual',
                'old_join_column': 'LoteAntigo',
                'ref_column': 'Lote'
            },
            {
                'base_table': 'Orcamento',
                'join_table': 'IFC_Projeto',
                'columns': ['Projeto', 'AGGP_Fustes', 'AGGP_VTCC', 'AGGDT'],
                'join_column': 'Projeto',
                'old_join_column': 'Projeto',
                'ref_column': 'Projeto'
            },
            {
                'base_table': 'Orcamento',
                'join_table': 'IFC_SubRegiao',
                'columns': ['ChaveSubRot', 'AGGSR_Fustes', 'AGGSR_VTCC', 'AGGDT'],
                'join_column': 'ChaveSubRot',
                'old_join_column': 'ChaveSubRot',
                'ref_column': 'ChaveSubRot'
            },
            {
                'base_table': 'Orcamento',
                'join_table': 'CadastroFlorestal',
                'columns': [
                    'Talhao', 'DCR_Projeto', 'DT_Plantio', 'ESP', 'DCR_MatGen', 'Area',
                    'DIST_LP', 'DIST_PFRod', 'DIST_PFFer', 'DIST_LFRod',
                    'DIST_Total'
                ],
                'join_column': 'TalhaoAtual',
                'old_join_column': 'TalhaoReferencia',
                'ref_column': 'Talhao'
            }
        ]
        # Iterate over the configurations and create the temporary tables
        for config in temp_table_configs:
            self.create_temp_table(
                base_table=config['base_table'],
                join_table=config['join_table'],
                columns=config['columns'],
                join_column=config['join_column'],
                old_join_column=config['old_join_column'],
                ref_column=config['ref_column']
            )
        self.create_and_populate_final_table()
        self.create_final_table_2()
        return self.ajuste_base()
