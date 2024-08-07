import sys
from PyQt5.QtWidgets import QDialog, QListWidget, QVBoxLayout, QPushButton, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox, QHBoxLayout, QSpinBox, QFormLayout
import pandas as pd


class SheetSelectionDialog(QDialog):
    def __init__(self, sheets, parent=None):
        super(SheetSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Sheet")
        self.layout = QVBoxLayout(self)

        self.listWidgetSheets = QListWidget(self)
        for sheet in sheets:
            self.listWidgetSheets.addItem(sheet)
        self.layout.addWidget(self.listWidgetSheets)

        self.buttonOk = QPushButton("OK", self)
        self.buttonOk.clicked.connect(self.accept)
        self.layout.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton("Cancel", self)
        self.buttonCancel.clicked.connect(self.reject)
        self.layout.addWidget(self.buttonCancel)

    def getSelectedSheet(self):
        selectedItems = self.listWidgetSheets.selectedItems()
        if selectedItems:
            return selectedItems[0].text()
        return None

    @staticmethod
    def openFileDialog(parent=None):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(parent, "Abrir arquivo de cubagem", "",
                                                  "Arquivos excel (*.xlsx);;All Files (*)", options=options)
        if filePath:
            return filePath
        return None

    @staticmethod
    def loadExcel(filePath, parent=None):
        xls = pd.ExcelFile(filePath)
        sheets = xls.sheet_names

        sheetDialog = SheetSelectionDialog(sheets, parent)
        if sheetDialog.exec_() == QDialog.Accepted:
            selectedSheet = sheetDialog.getSelectedSheet()
            if selectedSheet:
                # Load the selected sheet
                df = pd.read_excel(filePath, sheet_name=selectedSheet)
                # Now you can do something with the dataframe
                return df
        return None


class NumberSelectionDialog(QDialog):
    def __init__(self, max_columns, parent=None):
        super(NumberSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Number of Headers")
        self.layout = QVBoxLayout(self)

        self.spinBox = QSpinBox(self)
        self.spinBox.setRange(1, max_columns)
        self.layout.addWidget(QLabel("Select number of headers:"))
        self.layout.addWidget(self.spinBox)

        self.buttonOk = QPushButton("OK", self)
        self.buttonOk.clicked.connect(self.accept)
        self.layout.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton("Cancel", self)
        self.buttonCancel.clicked.connect(self.reject)
        self.layout.addWidget(self.buttonCancel)

    def getNumber(self):
        return self.spinBox.value()

    @staticmethod
    def openDialog(max_columns, parent=None):
        dialog = NumberSelectionDialog(max_columns, parent)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.getNumber()
        return None


class HeaderSelectionDialog(QDialog):
    def __init__(self, headers, header_names, parent=None):
        super(HeaderSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Headers")
        self.layout = QVBoxLayout(self)

        self.formLayout = QFormLayout()
        self.headerCombos = []

        for name in header_names:
            headerComboBox = QComboBox(self)
            headerComboBox.addItems(headers)
            self.headerCombos.append((name, headerComboBox))
            self.formLayout.addRow(QLabel(name), headerComboBox)

        self.layout.addLayout(self.formLayout)

        self.buttonOk = QPushButton("OK", self)
        self.buttonOk.clicked.connect(self.accept)
        self.layout.addWidget(self.buttonOk)

        self.buttonCancel = QPushButton("Cancel", self)
        self.buttonCancel.clicked.connect(self.reject)
        self.layout.addWidget(self.buttonCancel)

        self.setLayout(self.layout)

    def getHeaders(self):
        names = [name for name, combo in self.headerCombos]
        headers = [combo.currentText() for name, combo in self.headerCombos]
        return names, headers

    @staticmethod
    def openDialog(headers, header_names, parent=None):
        dialog = HeaderSelectionDialog(headers, header_names, parent)
        if dialog.exec_() == QDialog.Accepted:
            return dialog.getHeaders()
        return None, None