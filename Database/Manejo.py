import sqlite3
import pandas as pd


class Manejo:
    def __init__(self, db):
        self.db = db

    def connect(self):
        return sqlite3.connect(self.db)

    def create_table(self, column, base, column_type="FLOAT"):
        """
        Add a new column to an existing table if it does not already exist.

        Parameters:
        ----------
        table_name : str
            The name of the column to add.
        base : str
            The name of the existing table to which the column will be added.
        column_type : str, optional
            The data type of the new column (default is "FLOAT").
        """
        try:
            with self.connect() as conn:
                cur = conn.cursor()
                # Check if the column already exists
                cur.execute(f"PRAGMA table_info({base})")
                existing_columns = [column[1] for column in cur.fetchall()]

                if column not in existing_columns:
                    # Add the new column if it doesn't exist
                    cur.execute(f"""
                        ALTER TABLE {base}
                        ADD COLUMN {column} {column_type}
                    """)
        except sqlite3.Error as e:
            print(f"An error occurred while adding the column '{column}' to the table '{base}': {e}")

    def drop_table(self, table_name):
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
                print(f"Tabela '{table_name}' foi removida com sucesso.")
        except Exception as e:
            print(f"Erro ao remover a tabela '{table_name}': {e}")

    def list_tables(self):
        """
        Retrieve a list of all table names in the database.

        Returns:
        ----------
        list
            A list of table names in the database.
        """
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()
        return [table[0] for table in tables]

    def fetch_all(self, table, columns="*"):
        """
        Fetch all rows from the specified table.

        Parameters:
        ----------
        table : str
            The name of the table from which to fetch data.
        columns : str or list, optional
            The columns to fetch. Default is '*', which fetches all columns.

        Returns:
        ----------
        list
            A list of tuples representing the rows in the table.
        """
        if isinstance(columns, list):
            columns = ", ".join(columns)

        query = f"SELECT {columns} FROM {table};"
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
        return rows

    def insert_last_row_into_table(self, source_table, target_table):
        """
        Insert the last row from the source table into the target table.

        :param source_table: The name of the table from which to fetch the last row.
        :param target_table: The name of the table where the row will be inserted.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # Fetch the last row from the source table
                cursor.execute(f"SELECT * FROM {source_table} ORDER BY ROWID DESC LIMIT 1")
                last_row = cursor.fetchone()

                if last_row is None:
                    print(f"No rows found in '{source_table}'.")
                    return

                # Fetch the column names of the target table to match the number of values
                cursor.execute(f"PRAGMA table_info({target_table})")
                columns_info = cursor.fetchall()
                columns_count = len(columns_info)

                if len(last_row) != columns_count:
                    raise ValueError(f"The number of columns in '{source_table}' does not match '{target_table}'.")

                # Prepare the SQL insert statement with placeholders for each column
                placeholders = ', '.join(['?' for _ in range(columns_count)])
                insert_sql = f"INSERT INTO {target_table} VALUES ({placeholders})"

                # Insert the last row into the target table
                cursor.execute(insert_sql, last_row)
                conn.commit()

                print(f"Successfully inserted the last row from '{source_table}' into '{target_table}'.")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        except ValueError as ve:
            print(f"Value error: {ve}")

    def fetch_one(self, column, table, condition_column, condition_value):
        """
        Fetch a single value from a specified column in the table based on a condition.

        Parameters:
        ----------
        column : str
            The name of the column from which to fetch the value.
        table : str
            The name of the table from which to fetch data.
        condition_column : str
            The column name used in the WHERE clause to filter data.
        condition_value : any
            The value used to filter the data in the condition_column.

        Returns:
        ----------
        any
            The value from the specified column that matches the condition, or None if no match is found.
        """
        query = f"SELECT {column} FROM {table} WHERE {condition_column} = ?"
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(query, (condition_value,))
            result = cur.fetchone()
            return result[0] if result else None

    def fetch_all_one_column(self, table, column):
        """
        Fetch all values from a single column in the specified table.

        Parameters:
        ----------
        table : str
            The name of the table from which to fetch data.
        column : str
            The name of the column from which to fetch data.

        Returns:
        ----------
        list
            A list of values from the specified column.
        """
        return [row[0] for row in self.fetch_all(table, column)]

    def list_columns(self, table_name):
        """
        List all column names in a specified table.

        :param table_name: The name of the table to retrieve column names from.
        :return: A list of column names.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                # Execute the PRAGMA command to get column information
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns_info = cursor.fetchall()
                # Extract the column names from the information
                column_names = [column[1] for column in columns_info]
                return column_names
        except Exception as e:
            print(f"Erro ao listar colunas da tabela '{table_name}': {e}")
            return []

    def create_table_from_another(self, source_table, new_table, columns=None):
        """
        Create a new table from an existing table.

        Parameters:
        ----------
        source_table : str
            The name of the source table from which data will be copied.
        new_table : str
            The name of the new table to create.
        columns : list of str, optional
            A list of column names to copy from the source table. If None, all columns are copied.

        Raises:
        ----------
        sqlite3.Error:
            If an error occurs during the creation of the new table.
        """
        columns_str = ', '.join(columns) if columns else '*'

        create_table_query = f"""
            CREATE TABLE {new_table} AS
            SELECT {columns_str}
            FROM {source_table};
        """

        try:
            with self.connect() as conn:
                cur = conn.cursor()
                cur.execute(create_table_query)
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table '{new_table}': {e}")

    def create_table_with_repeated_rows(self, source_table, new_table, max_row_id):
        """
        Create a new table by repeating the rows of the source table until a certain row ID.
        The new table includes an 'id' column as an auto-incrementing primary key.
        If the table already exists, drop it first.

        :param source_table: The name of the existing table to copy the structure and data from.
        :param new_table: The name of the new table to create.
        :param max_row_id: The maximum row ID to copy data up to.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # Step 1: Drop the new_table if it already exists
                cursor.execute(f"DROP TABLE IF EXISTS {new_table}")

                # Step 2: Retrieve column names and types from the source table, excluding the primary key
                cursor.execute(f"PRAGMA table_info({source_table})")
                columns_info = cursor.fetchall()

                column_definitions = []
                columns_for_select = []
                for column in columns_info:
                    column_name = column[1]
                    data_type = column[2]

                    if column[5] == 1:  # This column is the primary key
                        continue

                    # Convert data types to SQLite types
                    if "INT" in data_type.upper():
                        sql_data_type = "INTEGER"
                    elif "CHAR" in data_type.upper() or "TEXT" in data_type.upper():
                        sql_data_type = "TEXT"
                    elif "DOUBLE" in data_type.upper() or "FLOAT" in data_type.upper() or "REAL" in data_type.upper():
                        sql_data_type = "REAL"
                    else:
                        sql_data_type = "TEXT"  # Fallback to TEXT if type is unknown

                    column_definitions.append(f'"{column_name}" {sql_data_type}')
                    columns_for_select.append(column_name)

                # Step 3: Define the new table with an 'id' primary key
                create_table_sql = f"""
                    CREATE TABLE {new_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        {', '.join(column_definitions)}
                    )
                """
                print("Create table SQL:", create_table_sql)  # Debugging output
                cursor.execute(create_table_sql)

                # Step 4: Retrieve the data up to max_row_id, excluding the primary key column
                select_columns_sql = ', '.join(columns_for_select)
                cursor.execute(f"SELECT {select_columns_sql} FROM {source_table} WHERE ROWID <= ?", (max_row_id,))
                rows = cursor.fetchall()
                print("Retrieved rows:", rows)  # Debugging output

                if not rows:
                    print(f"No data found up to ROWID {max_row_id} in '{source_table}'.")
                    return

                # Step 5: Insert the repeated rows into the new table
                placeholders = ', '.join(['?' for _ in columns_for_select])
                insert_sql = f"INSERT INTO {new_table} ({', '.join(columns_for_select)}) VALUES ({placeholders})"
                print("Insert SQL:", insert_sql)  # Debugging output

                repeated_rows = rows * 2  # Repeat the rows
                cursor.executemany(insert_sql, repeated_rows)

                print("Inserted rows count:", len(repeated_rows))  # Debugging output

                conn.commit()
                print(f"Tabela '{new_table}' criada com as linhas duplicadas até ROWID {max_row_id}.")
        except Exception as e:
            print(f"Erro ao criar a tabela '{new_table}': {e}")

    def update_column_based_on_another_table(self, target_table, target_column, source_table, source_column,
                                             primary_key):
        """
        Update the values in the target column of the target table with values from the source column of the source table,
        based on matching primary keys between the two tables.

        :param target_table: The name of the table where the values will be updated.
        :param target_column: The name of the column in the target table whose values will be updated.
        :param source_table: The name of the table from which the values will be copied.
        :param source_column: The name of the column in the source table from which the values will be copied.
        :param primary_key: The primary key column used to match rows between the two tables.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # SQL statement to update the target column with the source column's values
                update_sql = f"""
                    UPDATE {target_table} 
                    SET {target_column} = (
                        SELECT {source_column} 
                        FROM {source_table} 
                        WHERE {source_table}.{primary_key} = {target_table}.{primary_key}
                    )
                    WHERE EXISTS (
                        SELECT 1 
                        FROM {source_table} 
                        WHERE {source_table}.{primary_key} = {target_table}.{primary_key}
                    )
                """
                print("Executing SQL:", update_sql)  # Debugging output

                cursor.execute(update_sql)
                conn.commit()

                updated_rows = cursor.rowcount
                print(f"Rows updated: {updated_rows}")  # Debugging output

                if updated_rows > 0:
                    print(
                        f"Valores da coluna '{target_column}' em '{target_table}' foram atualizados com os valores da coluna '{source_column}' de '{source_table}'.")
                else:
                    print(f"Nenhuma linha foi atualizada. Verifique se as chaves primárias correspondem.")
        except Exception as e:
            print(f"Erro ao atualizar valores na coluna '{target_column}' de '{target_table}': {e}")

    def create_table_from_existing_schema(self, new_table_name, existing_table_name):
        """
        Create a new table based on the schema of an existing table.

        :param new_table_name: Name of the new table to be created.
        :param existing_table_name: Name of the existing table whose schema will be used.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # Check if the new table already exists
                cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{new_table_name}';")
                result = cursor.fetchone()

                if result:
                    print(f"Table '{new_table_name}' already exists.")
                else:
                    # Create the new table with the schema from the existing table
                    cursor.execute(f"CREATE TABLE {new_table_name} AS SELECT * FROM {existing_table_name} WHERE 0")

                    print(
                        f"Table '{new_table_name}' created successfully based on the schema of '{existing_table_name}'.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_summary_table_by_regiao(self, source_table, new_table, regiao_columns, row_x):
        """
        Create a new table where:
        - Each specified Regiao (from the regiao_columns) becomes a row in the new table.
        - Sums are calculated for each Regiao based on the specified columns.
        - For each Regiao, the sum of values up to row X (r1), the sum from row X+1 to the end (r2), and the total sum are calculated.

        :param source_table: The name of the existing table to copy the structure and data from.
        :param new_table: The name of the new table to create.
        :param regiao_columns: A list of region columns to sum.
        :param row_x: The row number (starting from 1) until which to sum the values.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()

                # Step 1: Drop the new_table if it already exists
                cursor.execute(f"DROP TABLE IF EXISTS {new_table}")

                # Step 2: Create the new table with columns for r1, r2, and their total
                create_table_sql = f"""
                    CREATE TABLE {new_table} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Regiao TEXT,
                        r1 REAL,
                        r2 REAL,
                        Total REAL
                    )
                """
                cursor.execute(create_table_sql)

                # Step 3: Calculate sums for each Regiao
                for regiao in regiao_columns:
                    # Sum up to row_x
                    cursor.execute(f"""
                        SELECT SUM({regiao}) 
                        FROM {source_table} 
                        WHERE ROWID <= ?
                    """, (row_x,))
                    sum_r1 = cursor.fetchone()[0] or 0

                    # Sum from row_x+1 to the end
                    cursor.execute(f"""
                        SELECT SUM({regiao}) 
                        FROM {source_table} 
                        WHERE ROWID > ?
                    """, (row_x,))
                    sum_r2 = cursor.fetchone()[0] or 0

                    total_sum = sum_r1 + sum_r2

                    # Step 4: Insert the calculated sums into the new table
                    insert_sql = f"""
                        INSERT INTO {new_table} (Regiao, r1, r2, Total)
                        VALUES (?, ?, ?, ?)
                    """
                    cursor.execute(insert_sql, (regiao, sum_r1, sum_r2, total_sum))

                conn.commit()

                print(f"Tabela '{new_table}' criada com somas para cada região até linha {row_x}.")

        except Exception as e:
            print(f"Erro ao criar a tabela '{new_table}': {e}")

    def ESPAreaBasal(self, table_name):
        self.create_table('EspAB', table_name)
        self.create_table('QTDArvIdeal', table_name)
        with self.connect() as conn:
            cur = conn.cursor()

            # Fetch relevant rows
            cur.execute(f"SELECT rowid, ESP FROM {table_name}")
            rows = cur.fetchall()

            # Prepare data for bulk update
            update_data = []
            for rowid, value in rows:
                if not value or value.lower() in ('', 'INDEFINIDO'):
                    result = 9.0
                else:
                    try:
                        num1, num2 = map(lambda x: float(x.replace(',', '.')), value.split(' X '))
                        result = round(num1 * num2, 1)
                    except ValueError as e:
                        print(f"Error processing value '{value}' for rowid {rowid}: {e}")
                        result = 9.0

                update_data.append((result, rowid))

            # Update 'esp_ab' column in bulk
            cur.executemany(f"UPDATE {table_name} SET EspAB = ? WHERE rowid = ?", update_data)

            # Calculate and update 'qtd_arv_ideal' based on 'esp_ab'
            cur.execute(f"""
                UPDATE {table_name}
                SET QTDArvIdeal = round(10000 / EspAB, 1)
                WHERE EspAB IS NOT NULL
            """)

    def Parameters(self, table_name, order_by_column=None):
        """
        Fetch the last row of a table in the database.

        :param table_name: The name of the table to fetch the last row from.
        :param order_by_column: The column to order by to determine the last row (e.g., an auto-incremented primary key).
        :return: The last row of the table as a tuple, or None if the table is empty.
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            if order_by_column:
                query = f"SELECT * FROM {table_name} ORDER BY {order_by_column} DESC LIMIT 1"
            else:
                # Fallback: If no order_by_column is provided, use the rowid
                query = f"SELECT * FROM {table_name} ORDER BY rowid DESC LIMIT 1"
            cursor.execute(query)
            return cursor.fetchone()

    def select_column_values(self, table_name, column_name):
        """
        Select and return all values from a specified column in a table.

        :param table_name: The name of the table to query.
        :param column_name: The name of the column to retrieve values from.
        :return: A list of values from the specified column.
        """
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                # Execute the SQL query to select the column values
                cursor.execute(f"SELECT {column_name} FROM {table_name}")
                # Fetch all the results
                rows = cursor.fetchall()
                # Extract the column values from the rows
                column_values = [row[0] for row in rows]
                return column_values
        except Exception as e:
            print(f"Erro ao selecionar valores da coluna '{column_name}' da tabela '{table_name}': {e}")
            return []

    def TaxaVPL(self, ref_, col_):
        juros = (float(self.Parameters('Parametros')[11]))/100
        ano_taxa = []
        for i in self.select_column_values(ref_, col_):
            taxa = 1 / (1 + juros) ** float(i)
            ano_taxa.append(taxa)
        return ano_taxa

    def CustosSilviculturaVPL(self, table_ref, new_table_name, col_):
        # Retrieve the 'ANO' column name and values
        ano_col = self.list_columns(table_ref)[2]
        ano_col_values = self.select_column_values(table_ref, ano_col)

        # Retrieve the other column names (regions)
        cols = self.list_columns(table_ref)[3:]

        # Calculate the TaxaVPL values
        taxas = self.TaxaVPL(table_ref, col_)

        # List to store all results
        all_results = []

        # Loop through each region, calculate the VPL results and store them
        for regiao in cols:
            vals = self.select_column_values(table_ref, regiao)
            result_values = [taxa * base_value for taxa, base_value in zip(taxas, vals)]
            all_results.append(result_values)

        # Combine 'ano_col_values' with 'all_results' into a DataFrame
        data = {ano_col: ano_col_values}
        for col, results in zip(cols, all_results):
            data[col] = results

        # Create the DataFrame
        df = pd.DataFrame(data)

        # Name of the new table
        new_table_name = new_table_name

        # Insert the DataFrame into the database as a new table
        try:
            with self.connect() as conn:
                # Save the DataFrame to the SQL database
                df.to_sql(new_table_name, conn, if_exists='replace', index=False)
                print(f"Tabela '{new_table_name}' criada com sucesso na base de dados.")
        except Exception as e:
            print(f"Erro ao criar a tabela '{new_table_name}': {e}")

    def ResInclinacao(self):
        """
        Create and update records in the 'ClassesInclinacaoResumo' table based on summarized regional data
        from the 'ClassesInclinacao' table. The function processes multiple fronts ('FRENTE') and
        updates corresponding areas and weighted values for inclination, and calculates the total.

        Process:
        ----------
        1. Inserts the specified 'headers' into the 'ClassesInclinacaoResumo' table under the 'FRENTE' column.
        2. For each 'frente' in 'updates', it updates the corresponding columns ('AREA', 'PD', 'GW_CE')
           in 'ClassesInclinacaoResumo' based on the summed values from the 'ClassesInclinacao' table.
           - 'AREA' is updated with the sum of areas for the specified regions.
           - 'PD' (pond_0_28) is updated with the sum of weighted values divided by the area.
           - 'GW_CE' (pond_29_mais) is updated similarly to 'PD'.
        3. Updates the 'TOTAL' column by summing 'GW_CE' and 'PD' and rounding to 4 decimal places.
        """

        headers = ['GN', 'BO', 'PO', 'CO', 'PI', 'SB', 'CNB']
        updates = [
            ("BO", ["BO", "IP"]),
            ("GN", ["SA", "VI"]),
            ("PO", ["PO"]),
            ("CO", ["CO"]),
            ("PI", ["PI"]),
            ("SB", ["SB"]),
            ("CNB", ["CNB"])
        ]

        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS ClassesInclinacaoResumo")
            cur.execute(
                """CREATE TABLE IF NOT EXISTS ClassesInclinacaoResumo(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                FRENTE TEXT,
                AREA FLOAT,
                PD FLOAT,
                GW_CE FLOAT,
                TOTAL FLOAT
                )"""
            )

            # Insert initial headers into 'ClassesInclinacaoResumo'
            cur.executemany(
                "INSERT INTO ClassesInclinacaoResumo (FRENTE) VALUES (?)",
                [(header,) for header in headers]
            )

            # Common update structure for AREA, PD, and GW_CE
            update_queries = [
                ("AREA", "SUM(ClassesInclinacao.Area)"),
                ("PD", "SUM(ClassesInclinacao.Pond0_28) / ClassesInclinacaoResumo.Area"),
                ("GW_CE", "SUM(ClassesInclinacao.Pond29_Mais) / ClassesInclinacaoResumo.Area")
            ]

            for frente, regioes in updates:
                regiao_conditions = " OR ".join([f"ClassesInclinacao.REGIAO = '{regiao}'" for regiao in regioes])

                for column, calculation in update_queries:
                    query = f'''
                        UPDATE ClassesInclinacaoResumo
                        SET {column} = (
                            SELECT {calculation}
                            FROM ClassesInclinacao
                            WHERE {regiao_conditions}
                        )
                        WHERE ClassesInclinacaoResumo.FRENTE = '{frente}'
                    '''
                    cur.execute(query)

            # Update the TOTAL column by summing GW_CE and PD
            cur.execute('''
                UPDATE ClassesInclinacaoResumo
                SET TOTAL = ROUND(GW_CE + PD, 4)
            ''')

            conn.commit()

    def CustosColheita(self, is_cnb=False):
        """
        Calculate the weighted (ponderado) costs for various 'custos_colheita' tables and update the tables accordingly.
        If 'is_cnb' is True, it calculates values specifically for the 'custos_colheita_cnb' table.

        Parameters:
        ----------
        is_cnb : bool, optional
            If True, calculates values for 'custos_colheita_cnb' by aggregating data from other tables (default is False).
        """

        tables = ['CustosColheitaBO', 'CustosColheitaCO', 'CustosColheitaGN', 'CustosColheitaPO',
                  'CustosColheitaSB', 'CustosColheitaPI']

        if is_cnb:
            memoria_vmi, memoria_pd, memoria_gw = [], [], []
            for table in tables:
                qry = table[-2:]
                area_frente = self.fetch_one('Area', 'ClassesInclinacaoResumo', 'FRENTE', qry)

                vmi_list = self.fetch_all_one_column(table, 'VMI')
                pd_list = self.fetch_all_one_column(table, 'PD')
                gw_list = self.fetch_all_one_column(table, 'GW')

                memoria_vmi.append([x[0] * area_frente for x in vmi_list])
                memoria_pd.append([x[0] * area_frente for x in pd_list])
                memoria_gw.append([x[0] * area_frente for x in gw_list])

            area_cnb = self.fetch_one('Area', 'ClassesInclinacaoResumo', 'FRENTE', 'CNB')
            summed_list_vmi = [sum(values) / area_cnb for values in zip(*memoria_vmi)]
            summed_list_pd = [sum(values) / area_cnb for values in zip(*memoria_pd)]
            summed_list_gw = [sum(values) / area_cnb for values in zip(*memoria_gw)]

            with self.connect() as conn:
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS CustosColheitaCNB AS SELECT * FROM CustosColheitaBOIP")
                for idx, (new_vmi, new_pd, new_gw) in enumerate(zip(summed_list_vmi, summed_list_pd, summed_list_gw)):
                    cur.execute(f"UPDATE CustosColheitaCNB SET VMI = ?, PD = ?, GW = ? WHERE id = ?",
                                (new_vmi, new_pd, new_gw, idx + 1))

            self._calcular_ponderado('CustosColheitaCNB', 'cnb')
        else:
            for table in tables:
                qry = table[-2:]
                self._calcular_ponderado(table, qry)

    def _calcular_ponderado(self, table, frente):
        """
        Calculate and update the weighted (ponderado) costs for a specific 'custos_colheita' table.

        Parameters:
        ----------
        table : str
            The name of the 'custos_colheita' table to update.
        frente : str
            The 'FRENTE' value used to fetch weighting factors from 'apoio_inclinacao'.
        """

        p_pd_frente = self.fetch_one('PD', 'ClassesInclinacaoResumo', 'FRENTE', frente)
        p_gw_ce_frente = self.fetch_one('GW_CE', 'ClassesInclinacaoResumo', 'FRENTE', frente)

        # Handle NoneType for p_pd_frente and p_gw_ce_frente
        p_pd_frente = p_pd_frente if p_pd_frente is not None else 0
        p_gw_ce_frente = p_gw_ce_frente if p_gw_ce_frente is not None else 0

        pd_list = self.fetch_all_one_column(table, 'PD')
        gw_list = self.fetch_all_one_column(table, 'GW')

        final_pd = [x * p_pd_frente if x is not None else 0 for x in pd_list]
        final_gw = [x * p_gw_ce_frente if x is not None else 0 for x in gw_list]
        ponderado_pd_gw = [pd + gw for pd, gw in zip(final_pd, final_gw)]

        with self.connect() as conn:
            cur = conn.cursor()

            # Check if the 'POND' column already exists
            cur.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cur.fetchall()]
            if 'POND' not in columns:
                cur.execute(f"ALTER TABLE {table} ADD COLUMN POND FLOAT")

            for idx, pond in enumerate(ponderado_pd_gw):
                cur.execute(f"UPDATE {table} SET POND = ? WHERE id = ?", (pond, idx + 1))

    def update_curva_and_vol7(self, table_name):
        """
        Update the 'curva', 'fator', and 'vol7' columns in the specified table.

        This function performs the following steps:
        1. Creates the 'curva', 'fator', and 'vol7' columns in the table if they do not already exist.
        2. Updates the 'curva' column based on the 'CurvaProdutividade' table.
        3. Updates the 'fator' column based on the values in the 'Curva' column.
        4. Updates the 'vol7' column based on the 'idade' and 'vtcc' columns.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Create necessary columns if they don't exist
        self.create_table('Curva', table_name)
        self.create_table('Fator', table_name)
        self.create_table('Vol7', table_name)

        # Mapping between regions in 'CurvaProdutividade' and the abbreviations in 'table_name.Regiao'
        region_map = {
            'Sabinopolis': 'SA',
            'Cocais': 'CO',
            'Piracicaba': 'PI',
            'SantaBarbara': 'SB',
            'BeloOriente': 'BO',
            'Ipaba': 'IP',
            'Pompeu': 'PO',
            'Virginopolis': 'VI'
        }

        with self.connect() as conn:
            cur = conn.cursor()

            # Update the 'Curva' column
            for region, abbreviation in region_map.items():
                cur.execute(f"""
                    UPDATE {table_name}
                    SET Curva = (
                        SELECT {region} FROM CurvaProdutividade
                        WHERE CurvaProdutividade.Idade = {table_name}.IdadeClasse
                    )
                    WHERE Regiao = '{abbreviation}' AND Curva IS NULL
                """)

            # Set 'Curva' to a default value of 130.00 if still NULL
            cur.execute(f"""
                UPDATE {table_name}
                SET Curva = 130.00
                WHERE Curva IS NULL
            """)

            # Update the 'Fator' column based on the 'Curva' values
            cur.execute(f"""
                UPDATE {table_name}
                SET Fator = CASE
                    WHEN Curva < 100 THEN 1.0 / (Curva / 100)
                    ELSE Curva / 100
                END
            """)

            # Update the 'Vol7' column based on 'Idade' and 'VTCC' values
            cur.execute(f"""
                UPDATE {table_name}
                SET Vol7 = CASE
                    WHEN Idade < 7 THEN VTCC * Fator
                    WHEN VTCC <> 0 THEN (1 - (Fator - 1)) * VTCC
                    ELSE 0
                END
            """)

    def perdas(self, table_name):
        """
        Updates the 'FatoresBrotacao' column in the specified table based on the 'Idade' column,
        calculates 'fatores_perdas_2', 'vol7_2c', and 'vol7_1c' based on specific conditions and values
        from related tables.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Create necessary columns if they don't exist
        self.create_table('FatoresBrotacao', table_name)
        self.create_table('FatoresTalhadia', table_name)
        self.create_table('Vol7_2ROT', table_name)
        self.create_table('Vol7_1ROT', table_name)

        with self.connect() as conn:
            cur = conn.cursor()

            # Update FatoresBrotacao
            cur.execute(f"""
                UPDATE {table_name}
                SET FatoresBrotacao = (
                    SELECT IndiceBrotacao.Perda 
                    FROM IndiceBrotacao
                    WHERE IndiceBrotacao.Idade <= {table_name}.Idade
                    ORDER BY IndiceBrotacao.Idade DESC
                    LIMIT 1
                )
                WHERE EXISTS (
                    SELECT 1 
                    FROM IndiceBrotacao
                    WHERE IndiceBrotacao.Idade <= {table_name}.Idade
                )
            """)

            cur.execute(f"""
                UPDATE {table_name}
                SET FatoresBrotacao = (
                    SELECT Perda 
                    FROM IndiceBrotacao
                    ORDER BY Idade ASC
                    LIMIT 1
                )
                WHERE FatoresBrotacao IS NULL
            """)

            # Fetch values from related tables
            perda = float(self.Parameters('Parametros')[2])

            r2 = float(self.Parameters('Parametros')[3])

            col = float(self.Parameters('Parametros')[13])

            value4 = float(self.Parameters('Parametros')[1])

            # Update fatores_perdas_2
            cur.execute(f"""
                UPDATE {table_name}
                SET FatoresTalhadia = CASE
                    WHEN Regime = 'R' THEN (FatoresBrotacao / 100) * ({perda} / 100) * ({r2} / 100) * ({col} / 100)
                    ELSE (FatoresBrotacao / 100) * ({perda} / 100) * ({col} / 100)
                END
            """)

            # Update vol7_2c
            cur.execute(f"""
                UPDATE {table_name}
                SET Vol7_2ROT = Vol7 * FatoresTalhadia
            """)

            # Update vol7_1c
            cur.execute(f"""
                UPDATE {table_name}
                SET Vol7_1ROT = Vol7 * {1 + (value4 / 100)}
            """)

        print(f"Updates for '{table_name}' completed: FatoresBrotacao, FatoresTalhadia, Vol7_2ROT, Vol7_1ROT.")

    def CustoMADPE(self, table_name, ref_vpl_table, total_table, new_column_name, vol_column_1, vol_column_2):
        """
        Generalized function to update the 'CustoMADPE' column in the specified table by calculating
        the cost based on data from the provided VPL and total cost tables.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        ref_vpl_table : str
            The name of the reference VPL table (e.g., 'CustosSilvicultura_REF_REG_VPL').
        total_table : str
            The name of the total cost table (e.g., 'CustosSilvicultura_REF_REG_VPL_Total').
        new_column_name : str
            The name of the new column to create and update (e.g., 'CustoMADPE_REF_REG').
        vol_column_1 : str
            The name of the first volume column (e.g., 'Vol7').
        vol_column_2 : str
            The name of the second volume column (e.g., 'Vol7_2ROT' or 'Vol7_1C').
        """
        # Ensure the target column exists
        self.create_table(new_column_name, table_name)

        with self.connect() as conn:
            cur = conn.cursor()

            # Fetch the required 'taxavpl' values in a single query
            taxas = self.TaxaVPL(ref_vpl_table, 'ANO')
            vpl7, vpl14 = float(taxas[7]), float(taxas[-1])

            # Prepare and execute the update statement
            cur.execute(f"""
                UPDATE {table_name}
                SET {new_column_name} = (
                    SELECT TOTAL
                    FROM {total_table}
                    WHERE {total_table}.Regiao = {table_name}.Regiao
                ) / ({vpl7} * {vol_column_1} + {vpl14} * {vol_column_2})
            """)

        print(f"Column '{new_column_name}' in table '{table_name}' has been updated.")

    def CustoTerra(self, table_name, cols, row_id):
        """
        Updates multiple columns in a specific row by summing the current value in each column with the corresponding 'Custo'
        value from the 'CustoTerra' table, where 'Regiao' matches the column names in 'table_name'.

        :param table_name: The name of the table to update.
        :param cols: A list of columns in 'table_name' to update.
        :param row_id: The identifier for the specific row in 'table_name' to update.
        """
        with self.connect() as conn:
            cur = conn.cursor()

            for col in cols:
                cur.execute(
                    f"""
                    UPDATE {table_name}
                    SET {col} = {col} + (
                        SELECT CustoTerra.Custo
                        FROM CustoTerra
                        WHERE CustoTerra.Regiao = ?
                    )
                    WHERE rowid = ? AND {col} IS NOT NULL
                    """, (col, row_id)
                )

            conn.commit()

    def CustosColheitaOP(self, table_name, ref_type, rot_type='2ROT', acrescimo_colheita=None):
        """
        Update columns related to the weighted costs of harvesting and calculate the final
        'CustosColheita' in the specified table, either for 'REF_REG' or 'REF_REF'.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        ref_type : str
            The reference type, either 'REG' or 'REF'.
        rot_type : str, optional
            The rotation type, '2ROT' for 'REF_REG' and '1ROT' for 'REF_REF' (default is '2ROT').
        acrescimo_colheita : float, optional
            The additional increase for 'REF_REF' calculations (default is None).
        """
        # Ensure the target columns exist
        self.create_table(f'CustosColheitaPond', table_name)
        self.create_table(f'CustosColheitaPond_{rot_type}', table_name)
        self.create_table(f'CustosColheita_{ref_type}', table_name)

        # Map regions to their corresponding 'custos_colheita' tables
        region_to_table_map = {
            'SA': 'CustosColheitaGN', 'VI': 'CustosColheitaGN',
            'BO': 'CustosColheitaBO', 'IP': 'CustosColheitaBO',
            'PO': 'CustosColheitaPO',
            'CO': 'CustosColheitaCO',
            'SB': 'CustosColheitaSB',
            'PI': 'CustosColheitaPI'
        }

        with self.connect() as conn:
            cur = conn.cursor()

            # Fetch the 'taxavpl' values from the nominal table for rowid 8 and 14
            taxas = self.TaxaVPL(f'CustosSilvicultura_{ref_type}_VPL', 'ANO')
            vpl7, vpl14 = float(taxas[7]), float(taxas[-1])

            # Update 'CustosColheitaPond' based on the mapping
            for regiao, colheita_table in region_to_table_map.items():
                cur.execute(f"""
                    UPDATE {table_name}
                    SET CustosColheitaPond = (
                        SELECT POND 
                        FROM {colheita_table} 
                        WHERE PROD <= Vol7 
                        ORDER BY PROD DESC LIMIT 1
                    )
                    WHERE Regiao = '{regiao}'
                """)

            # Update 'CustosColheitaPond_2ROT' or 'CustosColheitaPond_1ROT' similarly
            for regiao, colheita_table in region_to_table_map.items():
                cur.execute(f"""
                    UPDATE {table_name}
                    SET CustosColheitaPond_{rot_type}= (
                        SELECT POND 
                        FROM {colheita_table} 
                        WHERE PROD <= Vol7_{rot_type} 
                        ORDER BY PROD DESC LIMIT 1
                    )
                    WHERE Regiao = '{regiao}'
                """)

            # Calculate and update 'CustosColheita'
            if ref_type == 'REF_REF' and acrescimo_colheita:
                cur.execute(f"""
                    UPDATE {table_name}
                    SET CustosColheita_{ref_type} = (
                        Vol7 * CustosColheitaPond * {vpl7} + 
                        Vol7_{rot_type} * CustosColheitaPond_{rot_type} * {vpl14} * 
                        (1 + {acrescimo_colheita})
                    ) / (Vol7 * {vpl7} + Vol7_{rot_type} * {vpl14})
                """)
            else:
                cur.execute(f"""
                    UPDATE {table_name}
                    SET CustosColheita_{ref_type} = (
                        Vol7 * CustosColheitaPond * {vpl7} + 
                        Vol7_{rot_type} * CustosColheitaPond_{rot_type} * {vpl14}
                    ) / (Vol7 * {vpl7} + Vol7_{rot_type} * {vpl14})
                """)

        print(
            f"Columns 'CustosColheitaPond_{ref_type}', 'CustosColheitaPond_{rot_type}_{ref_type}', and 'CustosColheita_{ref_type}' in table '{table_name}' have been updated.")

    def CustosApoioColheita(self, table_name, ref_type, rot_type):
        """
        Update the 'apoio_col_ref_reg' column in the specified table by calculating
        the cost based on data from 'custos_silvicultura_nominal_ref_reg' and 'outros_custos'.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Ensure the target column exists
        self.create_table(f'CustosApoioColheita_{ref_type}', table_name)

        # Fetch the 'taxavpl' values from the nominal table for rowid 8 and 14
        taxas = self.TaxaVPL(f'CustosSilvicultura_{ref_type}_VPL', 'ANO')
        vpl7, vpl14 = float(taxas[7]), float(taxas[-1])

        with self.connect() as conn:
            cur = conn.cursor()

            # Prepare and execute the update statement
            cur.execute(f"""
                UPDATE {table_name}
                SET CustosApoioColheita_{ref_type} = (
                    SELECT (ApoioColheita * ({vpl7} + {vpl14})) / NULLIF(Vol7 * {vpl7} + Vol7_{rot_type} * {vpl14}, 0)
                    FROM OutrosCustos
                    WHERE OutrosCustos.Regiao = {table_name}.Regiao
                    LIMIT 1
                )
            """)

        print(f"Column 'CustosApoioColheita_{ref_type}' in table '{table_name}' has been updated.")

    def CustosColheitaEstradaInterna(self, table_name, ref_type, rot_type):
        """
        Update the 'CustosColheitaEstradaInterna_REF_REG' column in the specified table by calculating
        the cost based on data from 'custos_silvicultura_nominal_ref_reg' and 'outros_custos'.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Ensure the target column exists
        self.create_table(f'CustosColheitaEstradaInterna_{ref_type}', table_name)

        # Fetch the 'taxavpl' values from the nominal table for rowid 8 and 14
        taxas = self.TaxaVPL(f'CustosSilvicultura_{ref_type}_VPL', 'ANO')
        vpl7, vpl14 = float(taxas[7]), float(taxas[-1])

        with self.connect() as conn:
            cur = conn.cursor()

            # Prepare and execute the update statement
            cur.execute(f"""
                UPDATE {table_name}
                SET CustosColheitaEstradaInterna_{ref_type} = (
                    SELECT (EstInterna * ({vpl7} + {vpl14})) / NULLIF(Vol7 * {vpl7} + Vol7_{rot_type} * {vpl14}, 0)
                    FROM OutrosCustos
                    WHERE OutrosCustos.Regiao = {table_name}.Regiao
                    LIMIT 1
                )
            """)

        print(f"Column 'CustosColheitaEstradaInterna_{ref_type}' in table '{table_name}' has been updated.")

    def CustosColheitaTotal(self, table_name, ref_type):
        """
        Update the 'CustosColheitaTotal' column in the specified table by summing up
        the 'CustosColheita', 'CustosApoioColheita', and 'CustosColheitaEstradaInterna' columns.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Ensure the target column exists
        self.create_table(f'CustosColheitaTotal_{ref_type}', table_name)

        with self.connect() as conn:
            cur = conn.cursor()

            # Prepare and execute the update statement
            cur.execute(f"""
                UPDATE {table_name}
                SET CustosColheitaTotal_{ref_type} = 
                    COALESCE(CustosColheita_{ref_type}, 0) + 
                    COALESCE(CustosApoioColheita_{ref_type}, 0) + 
                    COALESCE(CustosColheitaEstradaInterna_{ref_type}, 0)
            """)

        print(f"Column 'CustosColheitaTotal_{ref_type}' in table '{table_name}' has been updated.")

    @staticmethod
    def combine_third_values(list1, list2):
        combined_dict = {}

        # Add values from the first list to the dictionary
        for item in list1:
            region = item[0]
            value = item[1]
            combined_dict[region] = value

        # Add values from the second list to the dictionary
        for item in list2:
            region = item[0]
            value = item[1]
            if region in combined_dict:
                combined_dict[region] += value
            else:
                combined_dict[region] = value

        # Convert the dictionary back to a list of tuples
        combined_list = [(region, round(combined_dict[region], 2)) for region in combined_dict]

        return combined_list

    def CustosTransporteGeral(self, table_name):
        """
        Update the 'custo_transporte', 'custo_estrada_ext', and 'custo_ferr_movpatio' columns in the specified table.
        This function handles transportation costs for road, external roads, and railway & patio movements.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Ensure necessary columns exist
        self.create_table('CustosTransporte', table_name)
        self.create_table('DistROD', table_name)
        self.create_table('CustoEstradaExterna', table_name)
        self.create_table('CustoFerroviariaMovPatio', table_name)

        with self.connect() as conn:
            cur = conn.cursor()

            # Update the 'DistROD' column based on distance calculations
            cur.execute(f"""
                UPDATE {table_name}
                SET DistROD = CASE 
                    WHEN DIST_LFRod = 0 THEN (DIST_LP + DIST_PFRod)
                    ELSE DIST_LFRod
                END
            """)

            # Mapping between region names and their corresponding codes
            region_map = {
                'Sabinopolis': 'SA',
                'Cocais': 'CO',
                'Piracicaba': 'PI',
                'SantaBarbara': 'SB',
                'BeloOriente': 'BO',
                'Ipaba': 'IP',
                'Pompeu': 'PO',
                'Virginopolis': 'VI'
            }

            # Update 'CustosTransporte' based on road distance
            for region_name, region_code in region_map.items():
                cur.execute(f"""
                    UPDATE {table_name}
                    SET CustosTransporte = (
                        SELECT {region_name} FROM CustosTransRod
                        WHERE CustosTransRod.Distancia = ROUND(({table_name}.DistROD + 2) / 5) * 5
                    )
                    WHERE Regiao = '{region_code}' AND CustosTransporte IS NULL
                """)

            # Update 'CustoEstradaExterna' based on region
            cur.execute(f"""
                UPDATE {table_name}
                SET CustoEstradaExterna = (
                    SELECT Custo FROM CustoEstExterna
                    WHERE CustoEstExterna.Regiao = {table_name}.Regiao
                )
            """)

            # Sum costs from 'CustoFerr' and 'MovPatio' tables and update the target table
            cur.execute("SELECT Regiao, Custo FROM CustoFerr")
            custos_ferr_vals = cur.fetchall()

            cur.execute("SELECT Regiao, Custo FROM CustoMovPatio")
            movpatio_vals = cur.fetchall()

            combined_vals = self.combine_third_values(custos_ferr_vals, movpatio_vals)

            # Update 'CustoFerroviariaMovPatio' based on region
            for region_code, total_cost in combined_vals:
                cur.execute(f"""
                    UPDATE {table_name}
                    SET CustoFerroviariaMovPatio = ?
                    WHERE Regiao = ?
                """, (total_cost, region_code))

        print(f"Transport costs updated for table '{table_name}'.")

    def OutrosCustos(self, table_name, ref_type, rot_type):
        """
        Updates the 'custo_taxa_adm_ref_reg' column in the specified table using administrative and tax costs
        from the 'outros_custos' table, weighted by the VPL values.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Ensure the target column exists
        self.create_table(f'CustosTAXAADM_{ref_type}', table_name)

        with self.connect() as conn:
            cur = conn.cursor()

            # Fetch the required 'taxavpl' values in a single query
            taxas = self.TaxaVPL(f'CustosSilvicultura_{ref_type}_VPL', 'ANO')
            vpl7, vpl14 = float(taxas[7]), float(taxas[-1])

            # Prepare and execute the update statement
            cur.execute(f"""
                UPDATE {table_name}
                SET CustosTAXAADM_{ref_type} = (
                    SELECT (ADM + Taxas) 
                    FROM OutrosCustos 
                    WHERE OutrosCustos.Regiao = {table_name}.Regiao
                ) * ({vpl7} + {vpl14}) / NULLIF(Vol7 * {vpl7} + Vol7_{rot_type} * {vpl14}, 0)
            """)

        print(f"Column 'CustosTAXAADM_{ref_type}' in table '{table_name}' has been updated.")

    def CustosPostoFabrica(self, table_name, ref_type):
        """
        Updates the 'CustosPostoFabrica_REF_REG' column in the specified table based on the region elevation.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        self.create_table(f'CustosPostoFabrica_{ref_type}', table_name)
        with self.connect() as conn:
            cur = conn.cursor()

            # Fetch the TRA and TRB parameters
            TRA = float(self.Parameters('Parametros')[4])
            TRB = float(self.Parameters('Parametros')[5])  # Assuming TRB should be fetched from index 5

            # Update the 'CustoPostoFabrica_REF_REG' column based on the 'Regiao' and its elevation category
            cur.execute(f"""
                UPDATE {table_name}
                SET CustosPostoFabrica_{ref_type} = 
                    CASE 
                        WHEN EXISTS (
                            SELECT 1 
                            FROM ELEVACAO 
                            WHERE ELEVACAO.Regiao = {table_name}.Regiao 
                            AND ELEVACAO.Elev = 'Região Baixa'
                        ) THEN (
                            COALESCE(CustoMADPE_{ref_type}, 0) + 
                            COALESCE(CustosColheitaTotal_{ref_type}, 0) + 
                            COALESCE(CustosTransporte, 0) + 
                            COALESCE(CustoEstradaExterna, 0) + 
                            COALESCE(CustoFerroviariaMovPatio, 0) + 
                            COALESCE(CustosTAXAADM_{ref_type}, 0)
                        ) * (100 - {TRB}) / 100
                        ELSE (
                            COALESCE(CustoMADPE_{ref_type}, 0) + 
                            COALESCE(CustosColheitaTotal_{ref_type}, 0) + 
                            COALESCE(CustosTransporte, 0) + 
                            COALESCE(CustoEstradaExterna, 0) + 
                            COALESCE(CustoFerroviariaMovPatio, 0) + 
                            COALESCE(CustosTAXAADM_{ref_type}, 0)
                        ) * (100 - {TRA}) / 100
                    END
            """)

        print(f"Column 'CustosPostoFabrica_{ref_type}' in table '{table_name}' has been updated.")

    def CustoMadAV(self, table_name):
        """
        Updates the 'custo_mad_av' column in the specified table by calculating
        the ratio of 'customad_posto_fabrica_ref_ref' to 'customad_posto_fabrica_ref_reg'.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Ensure the target column exists
        self.create_table('CustoMadAV', table_name)

        # Perform the update operation
        update_query = """
            UPDATE {table}
            SET CustoMadAV = 
                COALESCE(CustosPostoFabrica_REF_REF, 0) / NULLIF(CustosPostoFabrica_REF_REG, 0)
        """.format(table=table_name)

        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(update_query)

        print(f"'CustoMadAV' column in table '{table_name}' has been updated.")

    def AVUpdate(self, table_name, updates):
        """
        Update the specified columns in the table based on the provided update operations.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        updates : list of dict
            A list of dictionaries, each containing:
            - 'columns': List of column names to ensure exist in the table.
            - 'query': The SQL query to execute for the update.
        """
        # Ensure the target columns exist
        for update in updates:
            for column in update['columns']:
                self.create_table(column, table_name)

        with self.connect() as conn:
            cur = conn.cursor()
            for update in updates:
                cur.execute(update['query'])

        print(f"Table '{table_name}' has been updated with the specified operations.")

    def AVPipeline(self, table_name):
        """
        Perform the entire economic evaluation and update the table with the necessary columns.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        fave = (float(self.Parameters('Parametros')[12])) / 100
        ra3 = float(self.Parameters('Parametros')[6])
        rb3 = float(self.Parameters('Parametros')[7])
        ra2 = float(self.Parameters('Parametros')[8])
        rb2 = float(self.Parameters('Parametros')[9])

        updates = [
            {
                'columns': ['AVAreaReforma'],
                'query': f"""
                    UPDATE {table_name}
                    SET AVAreaReforma = CASE 
                        WHEN Vol7_2ROT = 0 OR CustoMadAV > {fave} THEN 0
                        ELSE Area
                    END
                """
            },
            {
                'columns': ['AvAreaNaoAvaliada'],
                'query': f"""
                    UPDATE {table_name}
                    SET AvAreaNaoAvaliada = CASE
                        WHEN CustoMadAV = 0 THEN Area
                        ELSE 0
                    END
                """
            },
            {
                'columns': ['AvAreaRegeneracao'],
                'query': f"""
                    UPDATE {table_name}
                    SET AvAreaRegeneracao = CASE
                        WHEN Vol7_2ROT = 0 OR CustoMadAV <= {fave} THEN 0
                        ELSE Area
                    END
                """
            },
            {
                'columns': ['RegAltaBaixa'],
                'query': f"""
                    UPDATE {table_name}
                    SET RegAltaBaixa = (
                        SELECT CASE 
                            WHEN Elevacao.Elev = 'REGIÃO BAIXA' THEN 'RB' 
                            ELSE 'RA' 
                        END
                        FROM Elevacao
                        WHERE Regiao = Elevacao.regiao
                    )
                """
            },
            {
                'columns': ['ArvMin', 'AvFustesAreaReforma'],
                'query': f"""
                    UPDATE {table_name}
                    SET ArvMin = CASE
                        WHEN RegAltaBaixa = 'RA' AND EspAB < 9 THEN {ra2}
                        WHEN RegAltaBaixa = 'RB' AND EspAB < 9 THEN {rb2}
                        WHEN RegAltaBaixa = 'RA' AND EspAB >= 9 THEN {ra3}
                        WHEN RegAltaBaixa = 'RB' AND EspAB >= 9 THEN {rb3}
                        ELSE ArvMin
                    END,
                    AvFustesAreaReforma = CASE
                        WHEN Fustes < ArvMin AND AvAreaRegeneracao > 0 THEN Area
                        ELSE 0
                    END
                """
            },
            {
                'columns': ['CloneSemente', 'AvCSAreaReforma'],
                'query': f"""
                    UPDATE {table_name}
                    SET CloneSemente = CASE
                        WHEN DCR_MatGen IN ('SEM0001', 'E-GRAND', 'E-RESIN', 'PINUS', 'E-GLOBU', 'E-UROPH', 'E-TOREL', 'E-SALIG') THEN 'Semente'
                        ELSE 'Clone'
                    END,
                    AvCSAreaReforma = CASE
                        WHEN AvFustesAreaReforma = 0 AND CloneSemente = 'Semente' THEN AvAreaRegeneracao
                        ELSE 0
                    END
                """
            },
            {
                'columns': ['AvR2AreaReforma'],
                'query': f"""
                    UPDATE {table_name}
                    SET AvR2AreaReforma = CASE
                        WHEN AvCSAreaReforma = 0 AND AvFustesAreaReforma = 0 AND Regime = 'R' THEN AvAreaRegeneracao
                        ELSE 0
                    END
                """
            },
            {
                'columns': ['FatorBrotacaoMatGen'],
                'query': f"""
                    UPDATE {table_name}
                    SET FatorBrotacaoMatGen = CASE
                        WHEN SUBSTR(Talhao, 5, 2) IN ('BA', 'MA') THEN (
                            SELECT RegBaixaEncosta
                            FROM RTMaterialGenetico
                            WHERE RTMaterialGenetico.DCR_MatGen = {table_name}.DCR_MatGen
                        )
                        WHEN SUBSTR(Talhao, 5, 2) = 'PD' THEN (
                            SELECT RegBaixaBaixada
                            FROM RTMaterialGenetico
                            WHERE RTMaterialGenetico.DCR_MatGen = {table_name}.DCR_MatGen
                        )
                        ELSE (
                            SELECT RegAlta
                            FROM RTMaterialGenetico
                            WHERE RTMaterialGenetico.DCR_MatGen = {table_name}.DCR_MatGen
                        )
                    END
                """
            },
            {
                'columns': ['AvMGNR'],
                'query': f"""
                    UPDATE {table_name}
                    SET AvMGNR = CASE
                        WHEN AvAreaRegeneracao > 0 AND AvFustesAreaReforma = 0 AND AvCSAreaReforma = 0 AND AvR2AreaReforma = 0 AND FatorBrotacaoMatGen = 0
                        THEN Area
                        ELSE 0
                    END
                """
            },
            {
                'columns': ['AvMaior15AreaReforma'],
                'query': f"""
                    UPDATE {table_name}
                    SET AvMaior15AreaReforma = CASE
                        WHEN Idade > 15 AND AvFustesAreaReforma = 0 AND AvCSAreaReforma = 0 AND AvR2AreaReforma = 0 AND AvMGNR = 0
                        THEN Area
                        ELSE 0
                    END
                """
            },
            {
                'columns': ['AvBaixaProd', 'ProdMin'],
                'query': f"""
                    UPDATE {table_name}
                    SET ProdMin = (
                        SELECT ProdMin 
                        FROM ProdMin 
                        WHERE ProdMin.Regiao = SUBSTR({table_name}.Talhao, 5, 2)
                    ),
                    AvBaixaProd = CASE
                        WHEN ProdMin > Vol7 AND AvFustesAreaReforma = 0 AND AvCSAreaReforma = 0 AND AvR2AreaReforma = 0 AND AvMGNR = 0 AND AvMaior15AreaReforma = 0
                        THEN Area
                        ELSE 0
                    END
                """
            },
            {
                'columns': ['AvAreaReformaSemi'],
                'query': f"""
                    UPDATE {table_name}
                    SET AvAreaReformaSemi = AvFustesAreaReforma + AvCSAreaReforma + AvR2AreaReforma + AvMGNR + AvMaior15AreaReforma
                """
            },
            {
                'columns': ['AvFinalNaoAvaliado', 'AvFinalAnalise', 'AvFinalReforma', 'AvFinalRegeneracao'],
                'query': f"""
                    UPDATE {table_name}
                    SET AvFinalNaoAvaliado = AvAreaNaoAvaliada,
                        AvFinalAnalise = AvBaixaProd,
                        AvFinalReforma = AvAreaReformaSemi + AvAreaReforma,
                        AvFinalRegeneracao = AvAreaRegeneracao - AvAreaReformaSemi - AvBaixaProd
                """
            }
        ]

        self.AVUpdate(table_name, updates)
        print(f"Table '{table_name}' has been fully updated with the economic evaluation pipeline.")

    def t700(self, table_name):
        """
        Update the specified table with the T700-related columns, including 'cod_projeto', 'cod_talhao',
        'cod_chave', 'cod_chave_ref', and 'remanescente'. The function processes these columns based on the
        structure of 'talhao_novo' and other conditions.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Ensure the target columns exist
        columns_to_create = ['cod_projeto', 'cod_talhao', 'cod_chave', 'cod_chave_ref', 'remanescente']
        for column in columns_to_create:
            self.create_table(column, table_name, 'TEXT')

        with self.connect() as conn:
            cur = conn.cursor()

            # Update 'cod_projeto', 'cod_talhao', and 'cod_chave'
            cur.execute(f"""
                UPDATE {table_name}
                SET cod_projeto = SUBSTR(Talhao, 1, 11),
                    cod_talhao = SUBSTR(Talhao, INSTR(Talhao, '-') + 1),
                    cod_chave = SUBSTR(Talhao, 1, 11) || SUBSTR(Talhao, INSTR(Talhao, '-') + 1)
            """)

            # Update 'remanescente'
            cur.execute(f"""
                UPDATE {table_name}
                SET remanescente = CASE 
                    WHEN SUBSTR(cod_talhao, 1, 1) IN ('7', '8') THEN 'Remanescente'
                    WHEN SUBSTR(Talhao, LENGTH(Talhao), 1) IN ('R', 'S') THEN 'Remanescente'
                    ELSE 'Talhão'
                END
            """)

            # Update 'cod_chave_ref'
            cur.execute(f"""
                UPDATE {table_name}
                SET cod_chave_ref = CASE
                    WHEN remanescente = 'Remanescente' THEN
                        CASE
                            WHEN SUBSTR(cod_talhao, 1, 1) IN ('7', '8') AND LENGTH(cod_chave) <= 14 THEN
                                SUBSTR(Talhao, 1, 11) || '0' || SUBSTR(Talhao, INSTR(Talhao, '-') + 2)
                            WHEN SUBSTR(cod_talhao, 1, 1) IN ('7', '8') AND LENGTH(cod_chave) > 14 THEN
                                SUBSTR(Talhao, 1, 11) || '0' || SUBSTR(Talhao, INSTR(Talhao, '-') + 2, LENGTH(Talhao) - INSTR(Talhao, '-') - 2)
                            WHEN SUBSTR(Talhao, LENGTH(Talhao), 1) IN ('R', 'S') THEN
                                SUBSTR(Talhao, 1, 11) || SUBSTR(Talhao, INSTR(Talhao, '-') + 1, LENGTH(Talhao) - INSTR(Talhao, '-') - 1)
                            ELSE NULL
                        END
                    ELSE NULL
                END
            """)

        print(f"Table '{table_name}' has been updated with T700-related columns.")

    def t700_organizador(self, table_name1, table_name2=None):
        """
        Update the 'manejo_final_apex' column in 'table_name1' based on the 'remanescente' status
        and the corresponding 'manejo_apex' value in 'table_name2'. If no match is found,
        the original 'manejo_apex' value from 'table_name1' is retained.

        If 'table_name2' is not provided, the function will directly copy 'manejo_apex' to 'manejo_final_apex'.

        Parameters:
        ----------
        table_name1 : str
            The name of the main table to update.
        table_name2 : str, optional
            The name of the secondary table from which to fetch the 'manejo_apex' value (default is None).
        """
        # Ensure the target column exists
        self.create_table('ManejoAPEX_Final', table_name1, 'TEXT')

        if table_name2:
            # If table_name2 is provided, update based on the remanescente status and cod_chave_ref
            update_query = f"""
                UPDATE {table_name1}
                SET ManejoAPEX_Final = CASE
                    WHEN remanescente = 'Remanescente' THEN (
                        SELECT ManejoAPEX 
                        FROM {table_name2} AS t2 
                        WHERE t2.cod_chave = {table_name1}.cod_chave_ref
                    )
                    ELSE ManejoAPEX
                END
            """
        else:
            # If table_name2 is not provided, just copy manejo_apex to manejo_final_apex
            update_query = f"""
                UPDATE {table_name1}
                SET ManejoAPEX_Final = ManejoAPEX
            """

        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(update_query)

            # Ensure that 'manejo_final_apex' is not NULL
            cur.execute(f"""
                UPDATE {table_name1}
                SET ManejoAPEX_Final = COALESCE(ManejoAPEX_Final, ManejoAPEX)
            """)

        print(f"'ManejoAPEX_Final' column in table '{table_name1}' has been updated.")

    def APEX(self, table_name):
        """
        Update the 'manejo_apex' column in the specified table based on the conditions of 'av_final_reforma'.

        Parameters:
        ----------
        table_name : str
            The name of the table to update.
        """
        # Ensure the target column exists
        self.create_table('ManejoAPEX', table_name)

        with self.connect() as conn:
            cur = conn.cursor()

            # Update 'manejo_apex' based on 'av_final_reforma'
            cur.execute(f"""
                UPDATE {table_name}
                SET ManejoAPEX = CASE
                    WHEN AvFinalReforma > 0 THEN 'Reforma'
                    ELSE 'Regeneração'
                END
            """)

        print(f"'ManejoAPEX' column in table '{table_name}' has been updated.")

    def Pipeline(self):
        print("Starting Pipeline")
        self.create_table_with_repeated_rows('CustosSilvicultura_REF_REG', 'CustosSilvicultura_REF_REF', 7)
        self.update_column_based_on_another_table('CustosSilvicultura_REF_REF', 'ANO', 'CustosSilvicultura_REF_REG',
                                                  'ANO', 'id')

        cols_to_update = ['BO', 'IP', 'PO', 'CO', 'PI', 'SB', 'SA', 'VI']
        self.CustoTerra('CustosSilvicultura_REF_REF', cols_to_update, 8)

        self.CustosSilviculturaVPL('CustosSilvicultura_REF_REG', 'CustosSilvicultura_REF_REG_VPL', 'ANO')
        self.CustosSilviculturaVPL('CustosSilvicultura_REF_REF', 'CustosSilvicultura_REF_REF_VPL', 'ANO')

        cols = self.list_columns('CustosSilvicultura_REF_REG')[3:]
        self.create_summary_table_by_regiao('CustosSilvicultura_REF_REG_VPL', 'CustosSilvicultura_REF_REG_VPL_Total', cols, 7)
        self.create_summary_table_by_regiao('CustosSilvicultura_REF_REF_VPL', 'CustosSilvicultura_REF_REF_VPL_Total',
                                            cols, 7)
        self.ResInclinacao()
        self.CustosColheita()

        n = len([x for x in self.list_tables() if x.startswith('Apex_Manejo')])
        goal = f'Apex_Manejo_{n+1}'
        self.create_table_from_another('apex_base_1', goal)
        self.ESPAreaBasal(goal)
        self.update_curva_and_vol7(goal)
        self.perdas(goal)

        self.CustoMADPE(
            table_name=goal,
            ref_vpl_table='CustosSilvicultura_REF_REG_VPL',
            total_table='CustosSilvicultura_REF_REG_VPL_Total',
            new_column_name='CustoMADPE_REF_REG',
            vol_column_1='Vol7',
            vol_column_2='Vol7_2ROT'
        )
        self.CustoMADPE(
            table_name=goal,
            ref_vpl_table='CustosSilvicultura_REF_REF_VPL',
            total_table='CustosSilvicultura_REF_REF_VPL_Total',
            new_column_name='CustoMADPE_REF_REF',
            vol_column_1='Vol7',
            vol_column_2='Vol7_1ROT'
        )
        acrescimo_colheita = (float(self.Parameters('Parametros')[10])) / 100
        self.CustosColheitaOP(
            table_name=goal,
            ref_type='REF_REG',
            rot_type='2ROT',
            acrescimo_colheita=acrescimo_colheita
        )
        self.CustosColheitaOP(
            table_name=goal,
            ref_type='REF_REF',
            rot_type='1ROT',
            acrescimo_colheita=acrescimo_colheita
        )
        self.CustosApoioColheita(
            table_name=goal,
            ref_type='REF_REG',
            rot_type='2ROT'
        )
        self.CustosApoioColheita(
            table_name=goal,
            ref_type='REF_REF',
            rot_type='1ROT'
        )
        self.CustosColheitaEstradaInterna(
            table_name=goal,
            ref_type='REF_REG',
            rot_type='2ROT'
        )
        self.CustosColheitaEstradaInterna(
            table_name=goal,
            ref_type='REF_REF',
            rot_type='1ROT'
        )
        self.CustosColheitaTotal(
            table_name=goal,
            ref_type='REF_REG',
        )
        self.CustosColheitaTotal(
            table_name=goal,
            ref_type='REF_REF',
        )
        self.CustosTransporteGeral(goal)
        self.OutrosCustos(
            table_name=goal,
            ref_type='REF_REG',
            rot_type='2ROT'
        )
        self.OutrosCustos(
            table_name=goal,
            ref_type='REF_REF',
            rot_type='1ROT'
        )
        self.CustosPostoFabrica(
            table_name=goal,
            ref_type='REF_REG'
        )
        self.CustosPostoFabrica(
            table_name=goal,
            ref_type='REF_REF'
        )
        self.CustoMadAV(goal)
        self.AVPipeline(goal)
        self.t700(goal)
        self.APEX(goal)
        # if self.rem:
        t_700 = f'Manejo_Apex_t700_{n + 1}'
        self.create_table_from_another(goal, t_700, ['Talhao', 'ManejoAPEX'])
        self.t700(t_700)
        self.t700_organizador(goal, t_700)
        # else:
        self.t700_organizador(goal, None)


db = Manejo(r'C:\Users\Leonardo\PycharmProjects\testes\Base_Testes_Valid_v02.db')
tables = [x for x in db.list_tables() if x.startswith('Manejo_Apex')]
for t in tables:
    print(t)
    db.drop_table(t)
