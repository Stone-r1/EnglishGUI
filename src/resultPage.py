from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QTextEdit, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QPointF, QRect
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QPixmap, QImage
import sys

class ResultWindow(QWidget):
    def __init__(self, startPage, wrongWords, timeElapsed, wrongWordsDict):
        super().__init__()
        self.startPage = startPage
        self.wrongWords = wrongWords
        self.wrongWordsDict = wrongWordsDict
        self.timeElapsed = timeElapsed
        self.UI()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")
        
        grid = QGridLayout()

        timeLabelA = QLabel(f"You finished the test in")
        timeLabelB = QLabel(f"{int(self.timeElapsed / 60)} minutes and {round(self.timeElapsed % 60, 1)} seconds") 

        timeLabelA.setStyleSheet("background: transparent; font-size: 20px;")
        timeLabelB.setStyleSheet("background: transparent; font-size: 20px;")

        scoreLabel = QLabel("You got " + str(20 - self.wrongWords) + " / 20 words right!")
        scoreLabel.setStyleSheet("background: transparent; font-size: 26px;")

        self.suggestionLabel = QLabel("Words to revise:")
        self.suggestionLabel.setStyleSheet("background: transparent;")
        self.wordsExist()

        maxLength = 45
        suggestionString = self.wrapText(self.wrongWordsDict, maxLength)

        reviseWordsLabel = QLabel(suggestionString)
        reviseWordsLabel.setStyleSheet("background: transparent; font-size: 12px") 
        reviseWordsLabel.setContentsMargins(0, 20, 0, 20)

        restartButton = QPushButton("Restart")
        restartButton.clicked.connect(self.restart) 

        returnButton = QPushButton("Return")
        returnButton.clicked.connect(self.mainMenuPage)

        grid.addWidget(timeLabelA, 1, 2, 1, 2)
        grid.addWidget(timeLabelB, 2, 2, 1, 2)
        grid.addWidget(scoreLabel, 3, 1, 1, 4)
        grid.addWidget(self.suggestionLabel, 4, 1, 1, 3)
        grid.addWidget(reviseWordsLabel, 5, 1, 2, 4)
        grid.addWidget(restartButton, 7, 1, 1, 2)
        grid.addWidget(returnButton, 7, 3, 1, 2)

        self.setLayout(grid) 
       

    def restart(self):
        self.startPage.resetUI()
        self.startPage.show()
        self.close() 


    def mainMenuPage(self):
        pass 

    
    def wordsExist(self):
        if not self.wrongWordsDict:
            self.suggestionLabel.setText(" ")


    def wrapText(self, wrongWordsDict, maxLength):
        suggestionString = ""
        for count, (key, value) in enumerate(list(wrongWordsDict.items())[:5]):
            entry = f"{key}: {value}"
            lines = []

            while len(entry) > maxLength:
                splitIndex = entry[:maxLength].rfind(" ")  # find last space within limit
                if splitIndex == -1:
                    splitIndex = maxLength
                    
                lines.append(entry[:splitIndex])
                entry = entry[splitIndex:].lstrip()

            lines.append(entry)
            suggestionString += "\n".join(lines) + "\n"  # Add a newline between entries

        return suggestionString

    
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
    window = ResultWindow()
    window.show()
    sys.exit(app.exec())
