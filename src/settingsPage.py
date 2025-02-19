from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPointF, QSize
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient

import sys

from startPage import StartWindow
from helpers.backgroundCanvas import BackgroundCanvas


class SettingsWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.UI()


    def UI(self): 
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower() 



if __name__ == "__main__":
    app = QApplication(sys.argv)
    settingsWindow = SettingsWindow()
    settingsWindow.show()
    sys.exit(app.exec())


