from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QTextEdit, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QPointF, QRect
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QPixmap, QImage

from helpers.backgroundCanvas import BackgroundCanvas
import sys


class ResultWindow(QWidget):
    def __init__(self, mainWindow, modeWindow, wrongWords, timeElapsed, wrongWordsDict, wordAmount):
        super().__init__()
        self.modeWindow = modeWindow
        self.mainWindow = mainWindow
        self.wrongWords = wrongWords
        self.wordAmount = wordAmount
        self.wrongWordsDict = wrongWordsDict
        self.timeElapsed = timeElapsed
        self.UI()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()
        
        grid = QGridLayout()

        timeLabelA = QLabel(f"You finished the test in")
        timeLabelB = QLabel(f"{int(self.timeElapsed / 60)} minutes and {round(self.timeElapsed % 60, 1)} seconds") 

        timeLabelA.setStyleSheet("background: transparent; font-size: 20px;")
        timeLabelB.setStyleSheet("background: transparent; font-size: 20px;")

        scoreLabel = QLabel("You got " + str(self.wordAmount - self.wrongWords) + " / " + str(self.wordAmount) + " words right!")
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
        if self.modeWindow:
            self.modeWindow.show()
        self.close() 


    def mainMenuPage(self):
        self.mainWindow.show()
        self.close()

    
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResultWindow()
    window.show()
    sys.exit(app.exec())
