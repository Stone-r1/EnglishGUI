from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit 
from PyQt6.QtCore import Qt, QPointF, QTimer, QTime
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
import sys
import subprocess
from resultPage import ResultWindow
import json


class StartWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.wordsDict = {}
        self.wrongWordsDict = {}
        self.wrongWord = 0
        self.once = True
        self.elapsedTime = QTime(0, 0, 0)
        self.currentWordIndex = 0
        self.currentWord = ""
        self.currentDefinition = ""

        self.UI()
        self.getWords() 


    def UI(self): 
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        gridLayout = QGridLayout()

        self.returnButton = QPushButton("Return")
        self.returnButton.clicked.connect(self.openMainWindow)

        self.definitionLabel = QLabel("Wait for 5 seconds... ")
        self.definitionLabel.setWordWrap(True)
        self.definitionLabel.setStyleSheet("font-size: 35px;")

        self.wordField = QLineEdit(self)
        self.wordField.setPlaceholderText("Write the word...")

        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.checkInfo)
        self.submitButton.setStyleSheet("font-size: 20px; ")
        self.submitButton.blockSignals(True)

        # stopwatch
        self.stopWatch = QTimer(self)
        self.stopWatch.timeout.connect(self.updateTime)

        self.time = QLabel("Starting in 5...", self)
        self.time.setStyleSheet("font-size: 16px;")
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # countdown
        self.delayTimer = QTimer(self)
        self.delayTimer.setSingleShot(True)
        self.delayTimer.timeout.connect(self.startStopWatch)
        self.delayTimer.start(5000)

        self.countdownTime = 5
        self.countdownTimer = QTimer(self)
        self.countdownTimer.timeout.connect(self.updateCountdown)
        self.countdownTimer.start(1000)

        gridLayout.addWidget(self.returnButton, 1, 1, 1, 1)
        gridLayout.addWidget(self.definitionLabel, 2, 1, 2, 4)
        gridLayout.addWidget(self.wordField, 4, 1, 2, 3)
        gridLayout.addWidget(self.submitButton, 4, 4, 2, 1)
        gridLayout.addWidget(self.time, 6, 4, 1, 1)

        self.setLayout(gridLayout) 

    
    def getWords(self):
        result = subprocess.run([sys.executable, "db/words.py", "1", "2", "START"], capture_output=True, text=True)
        self.wordsDict = json.loads(result.stdout)
        self.updateWord()


    def updateWord(self):
        if self.wordsDict:

            wordList = list(self.wordsDict.items())
            if self.currentWordIndex < len(wordList):
                self.currentWord, self.currentDefinition = wordList[self.currentWordIndex]
                self.definitionLabel.setText(self.currentDefinition)

            else:
                # close current page and open result page
                elapsedSeconds = QTime(0, 0, 0).secsTo(self.elapsedTime)
                self.resultWindow = ResultWindow(self, self.wrongWord, elapsedSeconds, self.wrongWordsDict) 
                self.resultWindow.show()
                self.close()
        
        else:
            self.definitionLabel.setText("No words available.")


    def checkInfo(self):
        userInput = self.wordField.text().strip()
        if userInput.lower() == self.currentWord.lower():
            self.currentWordIndex += 1
            self.once = True
            self.updateWord() 
            self.wordField.clear() 
            self.wordField.setStyleSheet("background-color: rgba(249, 205, 106, 0.5);")
        else:
            self.wrongWordsDict[self.currentWord] = self.currentDefinition
            self.wordField.clear()
            if self.once:
                self.wrongWord += 1
                self.once = False
            self.wordField.setStyleSheet("background-color: rgba(245, 63, 63, 0.5);")


    def updateCountdown(self):
        self.countdownTime -= 1
        if self.countdownTime > 0:
            self.time.setText(f"Starting in {self.countdownTime}...")
        else:
            self.countdownTimer.stop()


    def startStopWatch(self):
        self.stopWatch = QTimer(self)
        self.stopWatch.timeout.connect(self.updateTime)
        self.stopWatch.start(1000)
        self.time.setText("00:00:00")

        self.time.setStyleSheet("font-size: 24px;")
        self.submitButton.blockSignals(False)

    
    def updateTime(self):
        self.elapsedTime = self.elapsedTime.addSecs(1)
        self.time.setText(self.elapsedTime.toString("hh:mm:ss"))
        

    def stopStopWatch(self):
        self.stopWatch.stop()


    def openMainWindow(self):
        if self.mainWindow:
            self.mainWindow.show()
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
    window = StartWindow()
    window.show()
    sys.exit(app.exec())

