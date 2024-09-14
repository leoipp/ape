import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from Recursos.ui_setup import UiSetup
from Recursos.data_processing import DataProcessing
from Recursos.utility_functions import UtilityFunctions
from Dialogs.Create import CreateDataBase, OpenDataBase


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.dragPos = None

        self.utility_functions = UtilityFunctions(self)
        self.data_processing = DataProcessing(self)
        self.create_db = CreateDataBase(self)
        self.open_db = OpenDataBase(self)
        self.ui_setup = UiSetup(self)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if self.dragPos is not None:
                self.move(event.globalPos() - self.dragPos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPos = None
            event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())
