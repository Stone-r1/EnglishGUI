from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient

from addPage import AddWindow
from modePage import ModeWindow
from contentPage import ContentWindow

import sys

from helpers.backgroundCanvas import BackgroundCanvas
from helpers.mainPageStyleSheet import styleSheet


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

        self.decorations1 = QColor(156, 187, 252)
        self.decorations2 = QColor(156, 187, 252, 150)

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

        verticalLayout2.addWidget(startButton)
        verticalLayout2.setSpacing(10)
        verticalLayout2.addWidget(addButton)
        verticalLayout2.setSpacing(10)
        verticalLayout2.addWidget(contentButton)
        verticalLayout2.setContentsMargins(220, 0, 10, 30)

        verticalLayout.addLayout(verticalLayout2)
        self.setLayout(verticalLayout)


    def openAddWindow(self):
        self.addWindow = AddWindow(self)
        self.addWindow.show()
        self.close()


    def openModeWindow(self):
        self.modeWindow = ModeWindow(self)
        self.modeWindow.show()
        self.close()


    def openContentWindow(self):
        self.contentWindow = ContentWindow(self)
        self.contentWindow.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    window = Window()
    window.show()
    sys.exit(app.exec())

