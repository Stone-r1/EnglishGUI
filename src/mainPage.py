from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPointF, QSize
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient

from addPage import AddWindow
from modePage import ModeWindow
from contentPage import ContentWindow
from settingsPage import SettingsWindow

import sys

from helpers.backgroundCanvas import BackgroundCanvas
from helpers.mainPageStyleSheet import styleSheet
from helpers.moonButtonWidget import GradientButton


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        verticalLayout = QVBoxLayout()
        verticalLayout2 = QVBoxLayout()
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout2.setContentsMargins(0, 120, 0, 0)

        greeting = QLabel("<h1> Welcome! </h1>");
        greeting.setAlignment(Qt.AlignmentFlag.AlignRight)
        greeting.setStyleSheet("background: transparent;")
        greeting.setContentsMargins(0, 120, 0, 0)
        verticalLayout.addWidget(greeting)

        startButton = QPushButton("Start") 
        startButton.setObjectName("StartButton")
        startButton.clicked.connect(self.openModeWindow) 

        addButton = QPushButton("Add")
        addButton.setObjectName("AddButton")
        addButton.clicked.connect(self.openAddWindow) 

        contentButton = QPushButton("Words") 
        contentButton.setObjectName("AddButton")
        contentButton.clicked.connect(self.openContentWindow)

        settingsButton = GradientButton("+", self.background, self)
        settingsButton.setObjectName("SettingsButton")
        settingsButton.clicked.connect(self.openSettingsWindow)
        settingsButton.setGeometry(self.width() - 100, 30, 80, 80)

        verticalLayout2.addWidget(startButton)
        verticalLayout2.setSpacing(10)
        verticalLayout2.addWidget(addButton)
        verticalLayout2.setSpacing(10)
        verticalLayout2.addWidget(contentButton)
        verticalLayout2.setContentsMargins(220, 0, 10, 30)

        verticalLayout.addLayout(verticalLayout2)
        self.setLayout(verticalLayout)
        settingsButton.raise_()


    def openAddWindow(self):
        self.addWindow = AddWindow(self)
        self.addWindow.show()
        self.close()


    def openModeWindow(self):
        self.modeWindow = ModeWindow(self)
        self.modeWindow.show()
        self.close()


    def openSettingsWindow(self):
        self.settingsWindow = SettingsWindow(self)
        self.settingsWindow.show()
        self.close()


    def openContentWindow(self):
        self.contentWindow = ContentWindow(self)
        self.contentWindow.show()
        self.close()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main();
