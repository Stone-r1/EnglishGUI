from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
import subprocess


class AddWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.UI()


    def UI(self): 
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        grid = QGridLayout()

        returnButton = QPushButton("Return")
        returnButton.clicked.connect(self.openMainWindow)
        returnButton.setStyleSheet("font-size: 15px;")

        info = QLabel("<h1> You can add new words here </h1>") 
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("font-size: 11px;")

        wordLabel = QLabel("Word")
        self.wordInput = QLineEdit(self)
        self.wordInput.setPlaceholderText("Type something...")

        definitionLabel = QLabel("Definition") 
        self.definitionInput = QTextEdit(self)
        self.definitionInput.setPlaceholderText("Type something...")

        enterButton = QPushButton("Submit")
        enterButton.clicked.connect(self.gatherInfo)
        enterButton.setStyleSheet("font-size: 15px;")

        # just for grid
        expander = QWidget()
        expander.setStyleSheet("background: transparent;")
        expander.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


        grid.addWidget(returnButton, 0, 0, 1, 1)
        grid.addWidget(info, 1, 0, 1, 2)
        grid.addWidget(wordLabel, 2, 0)
        grid.addWidget(self.wordInput, 3, 0, 1, 2) 
        grid.addWidget(definitionLabel, 4, 0, 1, 0)
        grid.addWidget(self.definitionInput, 5, 0, 2, 4)
        grid.addWidget(enterButton, 7, 2)
        grid.addWidget(expander, 0, 3, 5, 2)

        self.setLayout(grid)

    
    def openMainWindow(self):
        if self.mainWindow:
            self.mainWindow.show()
        self.close()

    def gatherInfo(self):
        word = self.wordInput.text()
        definition = self.definitionInput.toPlainText()
        subprocess.run([sys.executable, "db/words.py", word, definition])

        self.wordInput.clear()
        self.definitionInput.clear()

    
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
    window = AddWindow()
    window.show();
    sys.exit(app.exec())
