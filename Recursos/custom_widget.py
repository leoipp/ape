from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMenu, QWidget, QVBoxLayout, QLabel, QSizePolicy


class CustomMenu(QMenu):
    def __init__(self, parent=None):
        """
        Custom QMenu with a specific appearance.
        """
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
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
                font-family: 'Corbel';
                font-size: 12pt;
                font-weight: bold;
                color: #000000;
            }
            QMenu::item:selected { 
                background-color: lightgray;
            }
        """)


class CustomMenuItem(QWidget):
    def __init__(self, text, parent=None):
        """
        Custom menu item with specific styling.
        """
        super().__init__(parent)
        layout = QVBoxLayout(self)
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont('Poppins', 12))
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        label.setFixedHeight(20)
        layout.addWidget(label)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def enterEvent(self, event):
        """
        Change background color on hover.
        """
        self.setStyleSheet("background-color: lightgray;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        """
        Reset background color when hover ends.
        """
        self.setStyleSheet("background-color: transparent;")
        super().leaveEvent(event)
