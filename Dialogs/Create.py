import os
from PyQt5 import QtWidgets, QtGui
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