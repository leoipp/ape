import sys
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMenu, QWidget, QLabel, QVBoxLayout, \
    QWidgetAction, QSizePolicy, QGraphicsDropShadowEffect, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic
from Database.Database import Database
from Gui.themes import *
from Dialogs.Open import SheetSelectionDialog, HeaderSelectionDialog
from Dialogs.Create import CreateDataBase, OpenDataBase
from Icons import icons


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
        uic.loadUi('teste.ui', self)  # Load the .ui file
        tabs = [
            self.tab_1, self.tab_2, self.tab_3, self.tab_4, self.tab_5,
            self.tab_6, self.tab_7, self.tab_8, self.tab_9, self.tab_10,
            self.tab_11, self.tab_12, self.tab_13, self.tab_14, self.tab_15
        ]
        for t in tabs:
            t.setShowGrid(False)
        self.apply_drop_shadow(self.frame_43)
        self.apply_drop_shadow(self.frame_42)
        self.apply_drop_shadow(self.frame_49)
        self.apply_drop_shadow(self.frame_50)
        self.apply_drop_shadow(self.frame_52)
        self.apply_drop_shadow(self.frame_53)
        self.apply_drop_shadow(self.frame_55)
        self.apply_drop_shadow(self.frame_56)

        self.apply_drop_shadow(self.Header)
        self.set_theme('light')

        self.create_db = CreateDataBase(self)
        self.open_db = OpenDataBase(self)

        # Create a custom menu
        self.menu_projeto = CustomMenu(self)
        self.menu_producao = CustomMenu(self)
        self.menu_cadastro = CustomMenu(self)
        self.menu_custos = CustomMenu(self)

        # Add custom widgets to the menu
        self.initialize_menus()

        # Connect the button's clicked signal to the show_menu method
        self.main_button_projeto.clicked.connect(lambda: self.show_menu(self.main_button_projeto, self.menu_projeto))
        self.main_button_producao.clicked.connect(lambda: self.show_menu(self.main_button_producao, self.menu_producao))

        self.toggle_button.clicked.connect(self.switch_theme)
        self.main_button_resultados.clicked.connect(lambda: self.dados_empilhados.setCurrentIndex(2))
        self.main_button_home.clicked.connect(lambda: self.dados_empilhados.setCurrentIndex(0))
        # List of button names
        button_names = {
            'button_open_1': ('IFC', self.tab_1, ['Talhao', 'DT_Medicao', 'Fustes', 'VTCC', 'Area']),
            'button_open_2': ('CurvaProdutividade', self.tab_3, ['Idade', 'Sabinópolis', 'Cocais', 'Piracicaba', 'Santa Bárbara', 'Belo Oriente', 'Ipaba', 'Pompéu', 'Virginópolis']),
            'button_open_3': ('RTMaterialGenetico', self.tab_4, ['DCR_MatGen', 'RegAlta', 'RegBaixaEncosta', 'RegBaixaBaixada']),
            'button_open_4': ('Orcamento', self.tab_5, ['TalhaoAtual', 'TalhaoReferencia']),
            'button_open_5': ('ClssesInclinacao', self.tab_6, ['Regiao', 'Area', 'HA0_28', 'HA29_38', 'HA38_MAIS', 'PCT0_28', 'PCT29_38', 'PCT38_MAIS']),
            'button_open_6': ('CadastroFlorestal', self.tab_7, ['Talhao', 'DCR_Projeto', 'DT_Plantio', 'ESP', 'DCR_MatGen', 'Area', 'DIST_LP', 'DIST_PFRod', 'DIST_PFFer', 'DIST_LFRod', 'DIST_Total']),
            'button_open_7': (),
            'button_open_8': ('CustosColheitaPI', self.tab_8, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_9': ('CustosColheitaPO', self.tab_9, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_10': ('CustosColheitaCO', self.tab_10, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_11': ('CustosColheitaGN', self.tab_11, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_12': ('CustosColheitaBOIP', self.tab_12, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_13': ('CustosColheitaSB', self.tab_13, ['PROD', 'VMI', 'PD', 'GW']),
            'button_open_14': ('CustosTransRod', self.tab_14, ['Distancia', 'Sabinópolis', 'Cocais', 'Piracicaba', 'Santa Bárbara', 'Belo Oriente', 'Ipaba', 'Pompéu', 'Virginópolis']),
            'button_open_15': ('OutrosCustos', self.tab_15, ['Regiao', 'ApoioColheita', 'EstInterna', 'EstExterna', 'MovPatio', 'ADM', 'Taxas']),
            'button_open_16': ('IFPC', self.tab_2, ['Talhao', 'DT_Medicao', 'Fustes', 'VTCC', 'Area'])
        }
        # Connect each button's clicked signal to the openFileDialog method
        for button_name, v in button_names.items():
            button = self.findChild(QPushButton, button_name)
            if button:
                button.clicked.connect(lambda _, v=v: self.openFileDialog(v[0], v[1], v[2]))

        self.label_base.textChanged.connect(self.atualizar_modelos)

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
        self.add_custom_menu_item('Compactar', self.option3_selected, self.menu_projeto)
        self.add_custom_menu_item('Database SQL', self.option3_selected, self.menu_projeto)
        self.add_custom_menu_item('Configurações', self.option3_selected, self.menu_projeto)

        self.add_custom_menu_item('Importação Cadastral', lambda: self.dados_empilhados.setCurrentIndex(1), self.menu_producao)
        self.add_custom_menu_item('Consistência', lambda: self.dados_empilhados.setCurrentIndex(0), self.menu_producao)

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

    def openFileDialog(self, table_name, table_widget, hder):
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
                    self.populate_table_from_db(db, table_name, table_widget)

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

    def populate_table_from_db(self, db, table_name, table_widget):
        df = db.fetch_all(table_name)
        self.populateTableWidget(df, table_widget)

    def atualizar_modelos(self):
        db = Database(self.label_base.text())
        tabelas = db.list_tables()

        tabs_in_app = {
            'IFC': self.tab_1, 'CurvaProdutividade': self.tab_3,
            'RTMaterialGenetico': self.tab_4, 'Orcamento': self.tab_5, 'ClssesInclinacao': self.tab_6,
            'CadastroFlorestal': self.tab_7, 'CustosColheitaPI': self.tab_8, 'CustosColheitaPO': self.tab_9,
            'CustosColheitaCO': self.tab_10, 'CustosColheitaGN': self.tab_11, 'CustosColheitaBOIP': self.tab_12,
            'CustosColheitaSB': self.tab_13, 'CustosTransRod': self.tab_14, 'OutrosCustos': self.tab_15,
            'IFPC': self.tab_2
        }
        for k, v in tabs_in_app.items():
            if k in tabelas:
                self.populate_table_from_db(db, k, v)
        print(tabelas)

    @staticmethod
    def option1_selected():
        print("Option 1 selected")

    @staticmethod
    def option2_selected():
        print("Option 2 selected")

    @staticmethod
    def option3_selected():
        print("Option 3 selected")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
