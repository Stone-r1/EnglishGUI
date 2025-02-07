from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient
from mainPageStyleSheet import styleSheet
from addPage import AddWindow
from modePage import ModeWindow
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

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

        verticalLayout2.addWidget(startButton)
        verticalLayout2.setSpacing(20)
        verticalLayout2.addWidget(addButton)
        verticalLayout2.setContentsMargins(220, 0, 10, 50)

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

    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) 
        painter.setPen(Qt.GlobalColor.transparent)

        # background
        gradient = QLinearGradient(QPointF(self.width(), 0), QPointF(0, self.height()))
        gradient.setColorAt(1, QColor("#388087"))
        gradient.setColorAt(0, QColor("#6FB3B8"))

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.drawRect(0, 0, self.width(), self.height())

        # big circle
        circle = QRadialGradient(QPointF(0, 0), 500)
        circle.setColorAt(1, QColor(185, 248, 255, 120))
        circle.setColorAt(0, QColor("#C2EDCE"))

        brush = QBrush(circle)
        painter.setBrush(brush)
        painter.drawEllipse(self.width() - 700, self.height() - 350, 500, 500)

        radialGradient = QRadialGradient(QPointF(self.width() - 30, 30), 100)
        radialGradient.setColorAt(0, QColor("#F6F6F2")) 
        radialGradient.setColorAt(1, QColor("#B9F8FF")) 

        brush = QBrush(radialGradient)
        painter.setBrush(brush)

        painter.drawEllipse(self.width() - 100, 30, 80, 80)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    window = Window()
    window.show()
    sys.exit(app.exec())

