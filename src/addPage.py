from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout,
    QTextEdit, QSizePolicy
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QKeyEvent
import sys
import subprocess


class CustomLineEdit(QLineEdit):
    def __init__(self, nextWidget = None, parent = None):
        super().__init__(parent)
        self.nextWidget = nextWidget

    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            event.accept()

            if self.nextWidget is not None:
                self.nextWidget.setFocus()

            return
        super().keyPressEvent(event)


class CustomTextEdit(QTextEdit):
    def __init__(self, autoSubmit = None, parent = None):
        super().__init__(parent)
        self.autoSubmit = autoSubmit


    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            event.accept()

            if self.autoSubmit is not None:
                self.autoSubmit()

            return
        super().keyPressEvent(event)


class AddWindow(QWidget):
    def __init__(self, mainWindow=None):
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

        definitionLabel = QLabel("Definition")
        # create a CustomTextEdit and pass gatherInfo as the callback for enter.
        self.definitionInput = CustomTextEdit(autoSubmit = self.gatherInfo, parent = self)
        self.definitionInput.setPlaceholderText("Type something...")
        self.definitionInput.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        wordLabel = QLabel("Word")
        self.wordInput = CustomLineEdit(nextWidget = self.definitionInput, parent = self)
        self.wordInput.setPlaceholderText("Type something...")
        self.wordInput.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.wordInput.setFocus()

        enterButton = QPushButton("Submit")
        enterButton.clicked.connect(self.gatherInfo)
        enterButton.setStyleSheet("font-size: 15px;")

        # Just for grid expansion.
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
        subprocess.run([sys.executable, "db/words.py", word, definition, "ADD"])

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
    window.show()
    sys.exit(app.exec())
