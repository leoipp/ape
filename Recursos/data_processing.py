import sqlite3

from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox

from Database.Consistencia import Consist
from Database.Database import Database


class DataProcessing:
    def __init__(self, main_window):
        """
        Handle all data processing tasks, including database operations and table updates.
        """
        self.main_window = main_window

    def connect_buttons(self, params):
        for button, (headers, labels_list, table_name) in params.items():
            button.clicked.connect(lambda _, h=headers, l=labels_list, t=table_name: self.handle_params_click(h, l, t))

    def handle_params_click(self, headers, labels_list, table_name):
        data = []

        # Loop through each list of labels
        for labels in labels_list:
            row_data = []
            for label in labels:
                if isinstance(label, QLabel):
                    text = float(label.text()) if label.text().strip() else 0.0
                elif isinstance(label, QComboBox):
                    text = label.currentText()
                elif isinstance(label, QLineEdit):
                    text = float(label.text()) if label.text().strip() else 0.0
                else:
                    text = ''  # Default to empty string if it's none of the above

                row_data.append(text)

            # Ensure the row_data length matches headers
            if len(row_data) != len(headers):
                raise ValueError("Each row of data must match the number of headers.")

            data.append(row_data)

        # Create or update the table in the database
        Database(self.main_window.label_base.text()).append_data_to_table(
            table_name, headers, data, parent=self.main_window
        )

    def prod_calc_click(self, headers, labels, tabela):
        data = []

        for label_id, label in labels:
            if isinstance(label, QLabel):
                text = float(label.text())
            elif isinstance(label, QComboBox):
                text = label.currentText()
            elif isinstance(label, QLineEdit):
                text = float(label.text())
            else:
                text = ''  # Default value if it's neither QLabel, QComboBox, nor QLineEdit

            data.append([label_id, text])

        Database(self.main_window.label_base.text()).create_table_with_data(
            tabela, headers, data, parent=self.main_window
        )

    def salvar_ajuste(self):
        """
        Save changes from the UI back to the database.
        """
        db = Database(self.main_window.label_base.text())
        df = db.fetch_all('apex_base_1', parent=self.main_window)
        self.main_window.primary_keys = df.iloc[:, 0].tolist()
        headers = [self.main_window.tab_consist.horizontalHeaderItem(i).text() for i in range(self.main_window.tab_consist.columnCount())]
        primary_key_column = headers[0]

        for row_idx in range(self.main_window.tab_consist.rowCount()):
            row_data = []
            for col_idx in range(self.main_window.tab_consist.columnCount()):
                item = self.main_window.tab_consist.item(row_idx, col_idx)
                row_data.append(item.text() if item else None)

            if row_idx < len(self.main_window.primary_keys):
                row_data.append(self.main_window.primary_keys[row_idx])
                db = Consist(self.main_window.label_base.text())
                db.save_changes_to_database('apex_base_1', row_data, primary_key_column, self.main_window.tab_consist)

    def atualizar_modelos(self):
        """
        Update the UI models based on the current state of the database.
        """
        db = Database(self.main_window.label_base.text())
        tabelas = db.list_tables()
        tabs_in_app = {
            'IFC': (self.main_window.tab_1, self.main_window.label_4), 'CurvaProdutividade': (self.main_window.tab_3, self.main_window.label_5),
            'RTMaterialGenetico': (self.main_window.tab_4, self.main_window.label_10), 'Orcamento': (self.main_window.tab_5, self.main_window.label_9),
            'ClassesInclinacao': (self.main_window.tab_6, self.main_window.label_8),
            'CadastroFlorestal': (self.main_window.tab_7, self.main_window.label_11), 'CustosColheitaPI': (self.main_window.tab_8, self.main_window.label_19),
            'CustosColheitaPO': (self.main_window.tab_9, self.main_window.label_20),
            'CustosColheitaCO': (self.main_window.tab_10, self.main_window.label_21), 'CustosColheitaGN': (self.main_window.tab_11, self.main_window.label_22),
            'CustosColheitaBO': (self.main_window.tab_12, self.main_window.label_18),
            'CustosColheitaSB': (self.main_window.tab_13, self.main_window.label_23), 'CustosTransRod': (self.main_window.tab_14, self.main_window.label_12),
            'OutrosCustos': (self.main_window.tab_15, self.main_window.label_15),
            'IFPC': (self.main_window.tab_2, self.main_window.label_3), 'CustosSilvicultura_REF_REG': (self.main_window.tab_22, self.main_window.label_13)
        }
        for k, v in tabs_in_app.items():
            if k in tabelas:
                self.main_window.utility_functions.populate_table_from_db(db, k, v[0], v[1])
