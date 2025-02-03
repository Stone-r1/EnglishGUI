from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient
from mainPageStyleSheet import styleSheet
from addPage import AddWindow
from startPage import StartWindow
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

        horizontalLayout = QHBoxLayout()
        verticalLayout = QVBoxLayout()
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)

        greeting = QLabel("<h1> Welcome! </h1>");
        greeting.setAlignment(Qt.AlignmentFlag.AlignCenter)
        greeting.setStyleSheet("background: transparent;")
        verticalLayout.addWidget(greeting)

        startButton = QPushButton("Start") 
        startButton.setObjectName("StartButton")
        startButton.clicked.connect(self.openStartWindow)

        addButton = QPushButton("Add")
        addButton.setObjectName("AddButton")
        addButton.clicked.connect(self.openAddWindow)

        horizontalLayout.addWidget(startButton)
        horizontalLayout.addWidget(addButton)
        horizontalLayout.setContentsMargins(0, 0, 0, 100)

        verticalLayout.addLayout(horizontalLayout)
        self.setLayout(verticalLayout)


    def openAddWindow(self):
        self.addWindow = AddWindow(self)
        self.addWindow.show()
        self.close()


    def openStartWindow(self):
        self.startWindow = StartWindow(self)
        self.startWindow.show()
        self.close()

    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) 
        painter.setPen(Qt.GlobalColor.transparent)
        
        gradient = QLinearGradient(QPointF(self.width(), 0), QPointF(0, self.height()))
        gradient.setColorAt(1, QColor("#F9CD6A"))
        gradient.setColorAt(0, QColor("#F6B420"))

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.drawRect(0, 0, self.width(), self.height())

        circle = QRadialGradient(QPointF(0, 0), 500)
        circle.setColorAt(1, QColor(156, 187, 252, 120))
        circle.setColorAt(0, QColor("#F6B420"))

        brush = QBrush(circle)
        painter.setBrush(brush)
        painter.drawEllipse(self.width() - 600, self.height() - 470, 500, 500)

        radialGradient = QRadialGradient(QPointF(self.width() - 30, 30), 100)
        radialGradient.setColorAt(0, QColor("#F6B420")) 
        radialGradient.setColorAt(1, QColor("#F9CD6A")) 

        brush = QBrush(radialGradient)
        painter.setBrush(brush)

        painter.drawEllipse(self.width() - 100, 30, 80, 80)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(styleSheet)
    window = Window()
    window.show()
    sys.exit(app.exec())

