from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit, QComboBox, QVBoxLayout
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QKeyEvent

import sys
import subprocess
import json

from helpers.backgroundCanvas import BackgroundCanvas
from helpers.mainPageStyleSheet import styleSheet
from startPage import StartWindow


class CustomLineEdit(QLineEdit):
    def __init__(self, checkValidity = None, parent = None): 
        super().__init__(parent)
        self.checkValidity = checkValidity

    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            event.accept()

            if self.checkValidity is not None:
                self.checkValidity()

            return
        super().keyPressEvent(event)


class ModeWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.categoryList = []
        self.amount = 0
        self.category = ""
        self.maxWords = 20

        self.UI()
        self.getCategories()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        grid = QGridLayout()
        grid.setVerticalSpacing(3)

        self.returnButton = QPushButton("Return")
        self.returnButton.clicked.connect(self.returnToMainWindow)

        categoryLabel = QLabel("Category")
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.setFixedWidth(250)
        self.categoryComboBox.addItem("ALL")

        wordAmountLabel = QLabel(" MAX 20")
        self.wordAmount = CustomLineEdit(checkValidity = self.checkValidity, parent = self)
        self.wordAmount.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.wordAmount.setFixedWidth(120)
        self.wordAmount.setPlaceholderText("Words")

        self.hardModeButton = QPushButton("HARD MODE")
        self.hardModeButton.clicked.connect(self.startHardMode) 
        self.hardModeButton.setStyleSheet("height: 50px; font-size: 24px;")

        hardModeLabel = QLabel("In Hard Mode 'Categories' is 'ALL' by default")
        instructionLabel = QLabel("Task is to finish quiz under x time")

        hardModeLabel.setStyleSheet("font-size: 12px; font-weight: 700;")
        instructionLabel.setStyleSheet("font-size: 14px;")

        labelContainer = QWidget()
        vbox = QVBoxLayout(labelContainer)
        vbox.setContentsMargins(0, 100, 0, 0)
        vbox.setSpacing(1)
        vbox.addWidget(hardModeLabel)
        vbox.addWidget(instructionLabel)
        labelContainer.setStyleSheet("background: transparent;")

        self.startButton = QPushButton("START")
        self.startButton.clicked.connect(self.checkValidity) # check if inputs are right first 


        grid.addWidget(self.returnButton, 0, 0, 1, 3) 

        grid.addWidget(categoryLabel, 1, 2, 1, 2, Qt.AlignmentFlag.AlignBottom)
        grid.addWidget(wordAmountLabel, 1, 0, 1, 2, Qt.AlignmentFlag.AlignBottom)

        grid.addWidget(self.categoryComboBox, 2, 2, 1, 3, Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.wordAmount, 2, 0, 1, 1, Qt.AlignmentFlag.AlignTop)

        grid.addWidget(labelContainer, 4, 0, 1, 4)
        grid.addWidget(self.hardModeButton, 5, 0, 1, 3)
        
        grid.addWidget(self.startButton, 5, 3, 1, 2)
        

        self.setLayout(grid)


    def returnToMainWindow(self):
        if self.mainWindow:
            self.mainWindow.show()
        self.close()


    def getCategories(self):
        result = subprocess.run([sys.executable, "db/words.py", "1", "2", "3", "4", "GET"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Subprocess error:", result.stderr)

        self.categoryList = json.loads(result.stdout)
        for i in self.categoryList:
            maxForCategory = subprocess.run([sys.executable, "db/words.py", "1", "2", i, "4", "COUNT"], capture_output=True, text=True)
            self.maxWords = json.loads(maxForCategory.stdout)
            self.categoryComboBox.addItem(i + "  ==  " + str(self.maxWords))


    def startOrdinaryMode(self):
        self.startWindow = StartWindow(self.mainWindow, self, self.amount, self.category)  
        self.startWindow.show()
        self.close()


    def checkValidity(self):
        self.amount = int(self.wordAmount.text())
        if self.amount > 20 or self.amount < 1:
            self.wordAmount.clear()
            self.wordAmount.setStyleSheet("background-color: rgba(245, 63, 63, 0.5);")
            self.wordAmount.setPlaceholderText("20!!!")
        else:
            self.category = self.categoryComboBox.currentText().split("  ==")[0].strip()
            maxForCategory = subprocess.run([sys.executable, "db/words.py", "1", "2", self.category, "4", "COUNT"], capture_output=True, text=True)
            self.maxWords = json.loads(maxForCategory.stdout) 
            if self.maxWords < self.amount:
                pass #warning
            else:
                self.startOrdinaryMode()

    
    def startHardMode(self):
        pass 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModeWindow()
    window.show()
    sys.exit(app.exec())
