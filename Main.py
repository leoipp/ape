import sqlite3
import sys
from functools import partial

from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QWidget, QLabel, QVBoxLayout, \
    QWidgetAction, QSizePolicy, QGraphicsDropShadowEffect, QTableWidgetItem, QHeaderView, QComboBox, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5 import uic

from Database.Consistencia import Consist
from Database.Database import Database
from Gui.themes import *
from Dialogs.Open import SheetSelectionDialog, HeaderSelectionDialog
from Dialogs.Create import CreateDataBase, OpenDataBase
from Icons import icons
import os


class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Apply a stylesheet to customize the menu appearance
        self.setStyleSheet("""
                    QMenu {
                        background-color: #FFFFFF;
                        border: none;
                        padding: 0px;
                        margin: 0px;
                    }
                    QMenu::item {
                        background-color: transparent;
                        padding: 8px 20px;
                        margin: 0px;
                        font-family: 'Corbel'; /* Set the font family */
                        font-size: 12pt; /* Set the font size */
                        font-weight: bold; /* Set the font weight to bold */
                        color: #000000; /* Set the font color */
                    }
                    QMenu::item:selected { 
                        background-color: lightgray;
                    }
                """)


class CustomMenuItem(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)

        # Set the font for the label
        font = QFont('Corbel', 12)
        self.label.setFont(font)

        # Adjust the size policy and minimum size
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label.setFixedHeight(20)

        layout.addWidget(self.label)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

    def enterEvent(self, event):
        self.setStyleSheet("background-color: lightgray;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: transparent;")
        super().leaveEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Gui/MainUI.ui', self)  # Load the .ui file

        self.side_bar.hide()
        self.set_theme('light')

        self.create_db = CreateDataBase(self)
        self.open_db = OpenDataBase(self)

        comboBoxes = [
            self.bo, self.ip, self.vi_2, self.sa_2,
            self.sb_2, self.pi, self.co, self.po_2
        ]
        for c in comboBoxes:
            c.addItems(['Região Alta', 'Região Baixa'])
        tabs = [
            self.tab_1, self.tab_2, self.tab_3, self.tab_4, self.tab_5,
            self.tab_6, self.tab_7, self.tab_8, self.tab_9, self.tab_10,
            self.tab_11, self.tab_12, self.tab_13, self.tab_14, self.tab_15,
            self.tab_22, self.tab_consist
        ]
        for t in tabs:
            t.setShowGrid(False)

        self.b1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.b2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.b3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.b4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.b5.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.b6.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.b7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.b8.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(7))
        self.b9.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(8))
        self.b10.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(10))
        self.b11.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(9))
        self.button_dados.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(0))
        self.button_consistencia.clicked.connect(lambda: self.stackedWidget_2.setCurrentIndex(1))

        self.button_consistir.clicked.connect(lambda: self.consist_bt())

        # Create a custom menu
        self.menu_projeto = CustomMenu(self)
        # Add custom widgets to the menu
        self.initialize_menus()

        # Connect the button's clicked signal to the show_menu method
        self.main_button_projeto.clicked.connect(lambda: self.show_menu(self.main_button_projeto, self.menu_projeto))
        self.toggle_button.clicked.connect(self.switch_theme)

        # List of button names
        button_names = {
            'button_open_1': ('IFC', self.tab_1, ['Talhao', 'DT_Medicao', 'Fustes', 'VTCC', 'Area'], self.label_4),
            'button_open_2': ('CurvaProdutividade', self.tab_3, ['Idade', 'Sabinópolis', 'Cocais', 'Piracicaba', 'Santa Bárbara', 'Belo Oriente', 'Ipaba', 'Pompéu', 'Virginópolis'], self.label_5),
            'button_open_3': ('RTMaterialGenetico', self.tab_4, ['DCR_MatGen', 'RegAlta', 'RegBaixaEncosta', 'RegBaixaBaixada'], self.label_10),
            'button_open_4': ('Orcamento', self.tab_5, ['TalhaoAtual', 'TalhaoReferencia'], self.label_9),
            'button_open_5': ('ClassesInclinacao', self.tab_6, ['Regiao', 'Area', 'HA0_28', 'HA29_38', 'HA38_MAIS', 'PCT0_28', 'PCT29_38', 'PCT38_MAIS'], self.label_8),
            'button_open_6': ('CadastroFlorestal', self.tab_7, ['Talhao', 'DCR_Projeto', 'DT_Plantio', 'ESP', 'DCR_MatGen', 'Area', 'DIST_LP', 'DIST_PFRod', 'DIST_PFFer', 'DIST_LFRod', 'DIST_Total'], self.label_11),
            'button_open_23': ('CustosSilvicultura', self.tab_22, ['Fase', 'ANO', 'BO', 'IP', 'PO', 'CO', 'PI', 'SB', 'SA', 'VI'], self.label_13),
            'button_open_8': ('CustosColheitaPI', self.tab_8, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_9': ('CustosColheitaPO', self.tab_9, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_10': ('CustosColheitaCO', self.tab_10, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_11': ('CustosColheitaGN', self.tab_11, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_12': ('CustosColheitaBOIP', self.tab_12, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_13': ('CustosColheitaSB', self.tab_13, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_14': ('CustosTransRod', self.tab_14, ['Distancia', 'Sabinópolis', 'Cocais', 'Piracicaba', 'Santa Bárbara', 'Belo Oriente', 'Ipaba', 'Pompéu', 'Virginópolis'], self.label_12),
            'button_open_15': ('OutrosCustos', self.tab_15, ['Regiao', 'ApoioColheita', 'EstInterna', 'EstExterna', 'MovPatio', 'ADM', 'Taxas'], self.label_15),
            'button_open_16': ('IFPC', self.tab_2, ['Talhao', 'DT_Medicao', 'Fustes', 'VTCC', 'Area'], self.label_3)
        }
        # Connect each button's clicked signal to the openFileDialog method
        for button_name, v in button_names.items():
            button = self.findChild(QPushButton, button_name)
            if button:
                button.clicked.connect(lambda _, v=v: self.openFileDialog(v[0], v[1], v[2], v[3]))

        self.label_base.textChanged.connect(self.atualizar_modelos)
        self.search_1.textChanged.connect(lambda text: self.search_in_table(text, self.tab_2))
        self.search_2.textChanged.connect(lambda text: self.search_in_table(text, self.tab_1))
        self.search_3.textChanged.connect(lambda text: self.search_in_table(text, self.tab_3))
        self.search_4.textChanged.connect(lambda text: self.search_in_table(text, self.tab_6))
        self.search_5.textChanged.connect(lambda text: self.search_in_table(text, self.tab_5))
        self.search_6.textChanged.connect(lambda text: self.search_in_table(text, self.tab_4))
        self.search_7.textChanged.connect(lambda text: self.search_in_table(text, self.tab_7))
        self.search_8.textChanged.connect(lambda text: self.search_in_table(text, self.tab_14))
        self.search_9.textChanged.connect(lambda text: self.search_in_table(text, self.tab_22))
        self.search_10.textChanged.connect(lambda text: self.search_in_table(text, self.tab_15))
        self.search_11.textChanged.connect(lambda text: self.search_in_table(text, self.tab_consist))

        self.cr.textChanged.connect(
            lambda: self.label_38.setText(self.prod_min(self.cr.text(), self.lineEdit_5.text())))
        self.pe.textChanged.connect(
            lambda: self.label_39.setText(self.prod_min(self.pe.text(), self.lineEdit_5.text())))
        self.sa.textChanged.connect(
            lambda: self.label_40.setText(self.prod_min(self.sa.text(), self.lineEdit_5.text())))
        self.ca.textChanged.connect(
            lambda: self.label_41.setText(self.prod_min(self.ca.text(), self.lineEdit_5.text())))
        self.ce.textChanged.connect(
            lambda: self.label_42.setText(self.prod_min(self.ce.text(), self.lineEdit_5.text())))
        self.al.textChanged.connect(
            lambda: self.label_43.setText(self.prod_min(self.al.text(), self.lineEdit_5.text())))
        self.it.textChanged.connect(
            lambda: self.label_44.setText(self.prod_min(self.it.text(), self.lineEdit_5.text())))
        self.pc.textChanged.connect(
            lambda: self.label_45.setText(self.prod_min(self.pc.text(), self.lineEdit_5.text())))
        self.sb.textChanged.connect(
            lambda: self.label_46.setText(self.prod_min(self.sb.text(), self.lineEdit_5.text())))
        self.pd.textChanged.connect(
            lambda: self.label_47.setText(self.prod_min(self.pd.text(), self.lineEdit_5.text())))
        self.po.textChanged.connect(
            lambda: self.label_48.setText(self.prod_min(self.po.text(), self.lineEdit_5.text())))
        self.ma.textChanged.connect(
            lambda: self.label_49.setText(self.prod_min(self.ma.text(), self.lineEdit_5.text())))
        self.ba.textChanged.connect(
            lambda: self.label_50.setText(self.prod_min(self.ba.text(), self.lineEdit_5.text())))
        self.vi.textChanged.connect(
            lambda: self.label_51.setText(self.prod_min(self.vi.text(), self.lineEdit_5.text())))

        self.lineEdit_5.textChanged.connect(self.update_all_labels)

        tabs_texto = {
            self.salvar_1: (['Regiao', 'ProdMin'],
                            [['CR', self.label_38], ['PE', self.label_39],
                             ['SA', self.label_40], ['CA', self.label_41],
                             ['CE', self.label_42], ['AL', self.label_43],
                             ['IT', self.label_44], ['PC', self.label_45],
                             ['SB', self.label_46], ['PD', self.label_47],
                             ['PO', self.label_48], ['MA', self.label_49],
                             ['BA', self.label_50], ['VI', self.label_51]],
                            'ProdMin'),
            self.salvar_2: (['Regiao', 'Elev'],
                            [
                                ['BO', self.bo],
                                ['IP', self.ip],
                                ['VI', self.vi_2],
                                ['SA', self.sa_2],
                                ['SB', self.sb_2],
                                ['PI', self.pi],
                                ['CO', self.co],
                                ['PO', self.po_2]
                            ], 'Elevacao'),
            self.salvar_3: (
                ['Regiao', 'Custo'],
                [
                    ['SB', self.lineEdit_8],
                    ['PI', self.lineEdit_7]
                ], 'CustoFerr'
            ),
            self.salvar_4: (
                ['Regiao', 'Custo'],
                [
                    ['SB', self.lineEdit_10],
                    ['PI', self.lineEdit_9]
                ], 'CustoMovPatio'
            ),
            self.salvar_5: (
                ['Regiao', 'Custo'],
                [
                    ['BO', self.est_bo_2],
                    ['IP', self.est_ip_2],
                    ['VI', self.est_vi_2],
                    ['SA', self.est_sa_2],
                    ['SB', self.est_sb_2],
                    ['PI', self.est_pi_2],
                    ['CO', self.est_co_2],
                    ['PO', self.est_po_2]
                ], 'CustoEstExterna'
            ),
            self.salvar_6: (
                ['Regiao', 'Custo'],
                [
                    ['BO', self.e_bo],
                    ['IP', self.e_ip],
                    ['PO', self.e_po],
                    ['CO', self.e_co],
                    ['PI', self.e_pi],
                    ['SB', self.e_sb],
                    ['SA', self.e_sa],
                    ['VI', self.e_vi]
                ], 'CustoTerra'
            )

        }
        for k, (headers, labels, tabela) in tabs_texto.items():
            k.clicked.connect(partial(self.prod_calc_click, headers, labels, tabela))

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

        Database(self.label_base.text()).create_table_with_data(
            tabela, headers, data
        )

    def set_theme(self, theme_name):
        if theme_name == 'light':
            self.setStyleSheet(light_theme)
        else:
            self.setStyleSheet(dark_theme)

    def switch_theme(self):
        # Check current theme and switch to the other
        current_stylesheet = self.styleSheet()
        if current_stylesheet == light_theme:
            self.set_theme('dark')
        else:
            self.set_theme('light')

    @staticmethod
    def apply_drop_shadow(widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(2)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)

    def initialize_menus(self):
        # Add custom widgets to the menu
        self.add_custom_menu_item('Novo', self.create_db.criar_base, self.menu_projeto)
        self.add_custom_menu_item('Abrir', self.open_db.open_base, self.menu_projeto)

    def add_custom_menu_item(self, text, callback, menu):
        action = QWidgetAction(menu)
        custom_widget = CustomMenuItem(text, self)
        action.setDefaultWidget(custom_widget)
        menu.addAction(action)
        custom_widget.mousePressEvent = lambda event: callback()

    @staticmethod
    def show_menu(botao, menu):
        # Show the menu below the button
        button_rect = botao.rect()
        menu_width = botao.width()  # Set the menu width to the button width
        global_pos = botao.mapToGlobal(button_rect.bottomLeft())
        menu.setFixedWidth(menu_width)  # Set the menu width to the button width
        menu.exec_(global_pos)

    def openFileDialog(self, table_name, table_widget, hder, label_shape):
        filePath = SheetSelectionDialog.openFileDialog(self)
        if filePath:
            df = SheetSelectionDialog.loadExcel(filePath, self)
            if df is not None:
                headers = df.columns.tolist()
                names, selected_headers = HeaderSelectionDialog.openDialog(headers, hder, self)
                if names and selected_headers:
                    df_selected = df[selected_headers]
                    df_selected.columns = names
                    db = Database(self.label_base.text())
                    db.create_table_from_dataframe(df_selected, table_name)
                    self.populate_table_from_db(db, table_name, table_widget, label_shape)

    def populateTableWidget(self, df, table_widget):
        table_widget.setRowCount(0)
        table_widget.setColumnCount(len(df.columns))
        table_widget.setHorizontalHeaderLabels(df.columns)

        for row_number, row_data in enumerate(df.values):
            table_widget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row_number, column_number, item)

        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def populate_table_from_db(self, db, table_name, table_widget, label_shape):
        df = db.fetch_all(table_name)
        label_shape.setText(str(df.shape))
        self.populateTableWidget(df, table_widget)

    def atualizar_modelos(self):
        db = Database(self.label_base.text())
        tabelas = db.list_tables()

        tabs_in_app = {
            'IFC': (self.tab_1, self.label_4), 'CurvaProdutividade': (self.tab_3, self.label_5),
            'RTMaterialGenetico': (self.tab_4, self.label_10), 'Orcamento': (self.tab_5, self.label_9), 'ClssesInclinacao': (self.tab_6, self.label_8),
            'CadastroFlorestal': (self.tab_7, self.label_11), 'CustosColheitaPI': (self.tab_8, self.label_19), 'CustosColheitaPO': (self.tab_9, self.label_20),
            'CustosColheitaCO': (self.tab_10, self.label_21), 'CustosColheitaGN': (self.tab_11, self.label_22), 'CustosColheitaBOIP': (self.tab_12, self.label_18),
            'CustosColheitaSB': (self.tab_13, self.label_23), 'CustosTransRod': (self.tab_14, self.label_12), 'OutrosCustos': (self.tab_15, self.label_15),
            'IFPC': (self.tab_2, self.label_3), 'CustosSilvicultura': (self.tab_22, self.label_13)
        }
        for k, v in tabs_in_app.items():
            if k in tabelas:
                self.populate_table_from_db(db, k, v[0], v[1])
        print(tabelas)

    @staticmethod
    def search_in_table(search_text, tabela):
        search_text = search_text.lower()
        for row in range(tabela.rowCount()):
            row_hidden = True
            for col in range(tabela.columnCount()):
                item = tabela.item(row, col)
                if item and search_text in item.text().lower():
                    row_hidden = False
                    break
            tabela.setRowHidden(row, row_hidden)

    @staticmethod
    def prod_min(prod, perda_percentual):
        try:
            # Convert inputs to floats
            prod_value = float(prod)
            perda_value = float(perda_percentual)

            # Calculate the resulting value considering percentage
            val = prod_value * (1 - perda_value / 100)

            # Format the result to avoid extra zeros
            return "{:.2f}".format(val)  # Format with two decimal places
        except ValueError:
            return "Invalid input"

    def update_all_labels(self):
        self.label_38.setText(self.prod_min(self.cr.text(), self.lineEdit_5.text()))
        self.label_39.setText(self.prod_min(self.pe.text(), self.lineEdit_5.text()))
        self.label_40.setText(self.prod_min(self.sa.text(), self.lineEdit_5.text()))
        self.label_41.setText(self.prod_min(self.ca.text(), self.lineEdit_5.text()))
        self.label_42.setText(self.prod_min(self.ce.text(), self.lineEdit_5.text()))
        self.label_43.setText(self.prod_min(self.al.text(), self.lineEdit_5.text()))
        self.label_44.setText(self.prod_min(self.it.text(), self.lineEdit_5.text()))
        self.label_45.setText(self.prod_min(self.pc.text(), self.lineEdit_5.text()))
        self.label_46.setText(self.prod_min(self.sb.text(), self.lineEdit_5.text()))
        self.label_47.setText(self.prod_min(self.pd.text(), self.lineEdit_5.text()))
        self.label_48.setText(self.prod_min(self.po.text(), self.lineEdit_5.text()))
        self.label_49.setText(self.prod_min(self.ma.text(), self.lineEdit_5.text()))
        self.label_50.setText(self.prod_min(self.ba.text(), self.lineEdit_5.text()))
        self.label_51.setText(self.prod_min(self.vi.text(), self.lineEdit_5.text()))

    def consist_bt(self):
        try:
            db = Consist(self.label_base.text())
            df = db.pipeline()
            self.populateTableWidget(df, self.tab_consist)
            self.label_25.setText(str(df.shape))
            vals = db.print_ajuste_base('apex_base_1')
            labs = [
                self.label_131,
                self.label_132,
                self.label_133,
                self.label_134,
                self.label_138,
                self.label_136,
                self.label_137,
                self.label_139,
                self.label_135,
                self.label_141
            ]
            for label, val in zip(labs, vals):
                label.setText(str(val))
        except sqlite3.OperationalError as op:
            print(op)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
