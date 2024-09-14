import os
from PyQt5 import QtWidgets, QtGui

from Database.Consistencia import Consist
from Database.Database import Database


class CreateDataBase:
    def __init__(self, parent=None):
        self.parent = parent

    def criar_base(self):
        try:
            base_path, _ = QtWidgets.QFileDialog.getSaveFileName(self.parent, "Criar Database", "./", "SQLite (*.db)")
            base_path = os.path.normpath(base_path)
            if not base_path or base_path == ".":
                return

            # Initialize the Database
            self.update_gui_with_database_path(base_path)
            self.show_success_message("Base de dados criada com sucesso!", "Criação de Database")

        except Exception as e:
            self.show_error_message(f"Erro ao criar a base de dados: {str(e)}", "Erro de Criação")

    def update_gui_with_database_path(self, base_path):
        self.parent.label_base.setText(base_path)
        # Create the database file by connecting to it
        db = Database(base_path)
        db.connect()
        return db

    def show_success_message(self, text, title):
        self.show_message(text, title, ":/svg/sucess.svg")

    def show_error_message(self, text, title):
        self.show_message(text, title, ":/svg/error.svg")

    def show_message(self, text, title, icon_path):
        msg = QtWidgets.QMessageBox(self.parent)
        icon = QtGui.QIcon(icon_path)
        msg.setWindowIcon(icon)
        icon_pixmap = QtGui.QPixmap(icon_path)
        msg.setIconPixmap(icon_pixmap)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()


class OpenDataBase:
    def __init__(self, parent=None):
        self.parent = parent

    def open_base(self):
        try:
            base_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.parent, "Abrir Database", "./", "SQLite (*.db)")
            base_path = os.path.normpath(base_path)
            if not base_path or base_path == ".":
                return

            # Initialize the Database
            self.update_gui_with_database_path(base_path)
            self.show_success_message("Base de dados aberta com sucesso!", "Abertura de Database")

        except Exception as e:
            self.show_error_message(f"Erro ao abrir a base de dados: {str(e)}", "Erro de Abertura")

    def update_gui_with_database_path(self, base_path):
        self.parent.label_base.setText(base_path)
        # Create the database file by connecting to it
        db = Database(base_path)
        db.connect()
        self.parent.apex_comp_1.addItems([x for x in db.list_apexes() if x.startswith('Apex_Manejo')])
        self.parent.apex_comp_2.addItems([x for x in db.list_apexes() if x.startswith('Apex_Manejo')])
        db.create_tabs_for_apex_manejo_tables(self.parent.utility_functions.add_new_tab)

        tables = [x for x in db.list_apexes() if x.startswith('Apex_Manejo')]
        if len([x for x in db.list_apexes() if x.startswith('Apex_Manejo')]) > 0:
            db = Consist(base_path)
            values = []
            for t in tables:
                values.append([
                    db.regional_resumo(t, 'Regeneração', 'SA', 3)/(db.regional_resumo(t, 'Regeneração', 'SA', 3)+db.regional_resumo(t, 'Reforma', 'SA', 3)),
                    db.regional_resumo(t, 'Regeneração', 'VI', 3)/(db.regional_resumo(t, 'Regeneração', 'VI', 3)+db.regional_resumo(t, 'Reforma', 'VI', 3)),
                    db.regional_resumo(t, 'Regeneração', 'CO', 3)/(db.regional_resumo(t, 'Regeneração', 'CO', 3)+db.regional_resumo(t, 'Reforma', 'CO', 3)),
                    db.regional_resumo(t, 'Regeneração', 'PI', 3)/(db.regional_resumo(t, 'Regeneração', 'PI', 3)+db.regional_resumo(t, 'Reforma', 'PI', 3)),
                    db.regional_resumo(t, 'Regeneração', 'SB', 3)/(db.regional_resumo(t, 'Regeneração', 'SB', 3)+db.regional_resumo(t, 'Reforma', 'SB', 3)),
                    db.regional_resumo(t, 'Regeneração', 'IP', 3)/(db.regional_resumo(t, 'Regeneração', 'IP', 3)+db.regional_resumo(t, 'Reforma', 'IP', 3)),
                    db.regional_resumo(t, 'Regeneração', 'PO', 3)/(db.regional_resumo(t, 'Regeneração', 'PO', 3)+db.regional_resumo(t, 'Reforma', 'PO', 3))])

            categories = ['Sabinópolis', 'Virginópolis', 'Cocais', 'Piracicaba', 'Santa Bárbara', 'Ipaba', 'Pompéu']
            self.parent.utility_functions.plot_radar_chart(self.parent.plotRadarChart, categories, values, 'Percentual de Talhadia (%)', tables)
        else:
            pass
        return db

    def show_success_message(self, text, title):
        self.show_message(text, title, ":/svg/sucess.svg")

    def show_error_message(self, text, title):
        self.show_message(text, title, ":/svg/error.svg")

    def show_message(self, text, title, icon_path):
        msg = QtWidgets.QMessageBox(self.parent)
        icon = QtGui.QIcon(icon_path)
        msg.setWindowIcon(icon)
        icon_pixmap = QtGui.QPixmap(icon_path)
        msg.setIconPixmap(icon_pixmap)
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()