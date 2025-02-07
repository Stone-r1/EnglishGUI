"""
TODO: 
    this page is to choose game mode.
    main idea:
        choose how many words will be in quiz
        choose category from which words will be gathered

        preferably: hard mode (you're limited in time) and background changes color to red
        time can be chosen manually, category will be ALL by default

        hmm other ideas later
"""

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit, QComboBox, QVBoxLayout
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QKeyEvent
import sys


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
        self.UI()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        grid = QGridLayout()
        grid.setVerticalSpacing(3)

        self.returnButton = QPushButton("Return")
        self.returnButton.clicked.connect(self.returnToMainWindow)

        categoryLabel = QLabel("Category")
        self.categoryList = QComboBox()
        self.categoryList.addItems(["Week 1", "Week 2", "Week 3"])
        self.categoryList.setFixedWidth(250)
        # gotta add items later

        wordAmountLabel = QLabel(" MAX 20")
        self.wordAmount = CustomLineEdit()
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

        grid.addWidget(self.categoryList, 2, 2, 1, 3, Qt.AlignmentFlag.AlignTop)
        grid.addWidget(self.wordAmount, 2, 0, 1, 1, Qt.AlignmentFlag.AlignTop)

        grid.addWidget(labelContainer, 4, 0, 1, 4)
        grid.addWidget(self.hardModeButton, 5, 0, 1, 3)
        
        grid.addWidget(self.startButton, 5, 3, 1, 2)
        

        self.setLayout(grid)


    def returnToMainWindow(self):
        if self.mainWindow:
            self.mainWindow.show()
        self.close()


    def checkValidity(self):
        pass

    
    def startHardMode(self):
        pass

    
    def startOrdinaryMode(self):
        pass
        
    

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
    window = ModeWindow()
    window.show()
    sys.exit(app.exec())
