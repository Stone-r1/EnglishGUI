from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QTextEdit 
from PyQt6.QtCore import Qt, QPointF, QTimer, QTime
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QKeyEvent

from helpers.backgroundCanvas import BackgroundCanvas
from resultPage import ResultWindow

import sys
import subprocess
import json


class CustomLineEdit(QLineEdit):
    def __init__(self, autoAccept = None, parent = None):
        super().__init__(parent) 
        self.autoAccept = autoAccept

    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            event.accept()

            if self.autoAccept is not None:
                self.autoAccept()

            return
        super().keyPressEvent(event)


class StartWindow(QWidget):
    def __init__(self, mainWindow, modeWindow, wordAmount, category, mode):
        super().__init__()
        self.modeWindow = modeWindow
        self.mainWindow = mainWindow
        self.mode = mode
        self.wordsDict = {}
        self.wrongWordsDict = {}
        self.wrongWord = 0
        self.once = True
        self.countdownFinished = False
        self.elapsedTime = QTime(0, 0, 0)
        self.currentWordIndex = 0
        self.currentWord = ""
        self.currentDefinition = ""
        self.wordAmount = wordAmount
        self.category = category

        self.UI() 
        self.getWords() 


    def UI(self): 
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        gridLayout = QGridLayout()

        self.returnButton = QPushButton("Return")
        self.returnButton.clicked.connect(self.openModeWindow)

        self.definitionLabel = QLabel("Wait for 5 seconds... ")
        self.definitionLabel.setWordWrap(True)
        self.definitionLabel.setStyleSheet("font-size: 35px;")

        self.wordField = CustomLineEdit(autoAccept = self.checkInfo, parent = self)
        self.wordField.setPlaceholderText("Write the word...")
        self.wordField.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.submitButton = QPushButton("Submit")
        self.submitButton.clicked.connect(self.checkInfo)
        self.submitButton.setStyleSheet("font-size: 20px; ")
        self.submitButton.blockSignals(True)

        # stopwatch / timer
        self.stopWatch = QTimer(self)

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
        result = subprocess.run([sys.executable, "db/words.py", "1", "2", self.category, str(self.wordAmount), "START"],capture_output=True,text=True) 
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
                self.resultWindow = ResultWindow(self.mainWindow, self.modeWindow, self.wrongWord, elapsedSeconds, self.wrongWordsDict, self.wordAmount, self.mode, True) 
                self.resultWindow.show()
                self.close()
        
        else:
            self.definitionLabel.setText("No words available.")


    def checkInfo(self):
        if self.countdownFinished == False:
            return

        userInput = self.wordField.text().strip()
        if userInput.lower() == self.currentWord.lower():
            self.currentWordIndex += 1
            self.once = True
            self.updateWord() 
            self.wordField.clear() 
            self.wordField.setStyleSheet("background-color: rgba(194, 237, 206, 0.5);")
        else:
            self.wrongWordsDict[self.currentWord] = self.currentDefinition
            self.wordField.clear()
            if self.once:
                self.wrongWord += 1
                self.once = False
            self.wordField.setStyleSheet("background-color: rgba(255, 51, 51, 0.5);")


    def updateCountdown(self):
        if not self.countdownFinished:
            # countdownTime counts down from 5 to 0.
            if self.countdownTime > 0:
                self.time.setText(f"Starting in {self.countdownTime}...")
                self.countdownTime -= 1
            else:
                # INITIAL countdown finished.
                self.countdownFinished = True
                if self.mode == "HARD":
                    # Set game duration.
                    self.elapsedTime = QTime(0, 2, 0)
                    self.time.setText(self.elapsedTime.toString("hh:mm:ss")) 
                    self.time.setStyleSheet("font-size: 24px;")

        elif self.mode == "HARD":
            # Game timer phase 
            if self.elapsedTime == QTime(0, 0, 0):
                self.time.setText("00:00:00")
                self.countdownTimer.stop()

                message = "FAIL"
                self.resultWindow = ResultWindow(self.mainWindow, self.modeWindow, self.wrongWord, message, self.wrongWordsDict, self.wordAmount, self.mode, False)
                self.resultWindow.show()
                self.close()

            else: 
                self.elapsedTime = self.elapsedTime.addSecs(-1)
                self.time.setText(self.elapsedTime.toString("hh:mm:ss"))


    def startStopWatch(self):
        if self.mode != "HARD":
            self.stopWatch = QTimer(self)
            self.stopWatch.timeout.connect(self.updateTimeStopwatch)
            self.stopWatch.start(1000)
            self.time.setText("00:00:00")

            self.time.setStyleSheet("font-size: 24px;")
            self.submitButton.blockSignals(False)

    
    def updateTimeStopwatch(self):
        self.elapsedTime = self.elapsedTime.addSecs(1)
        self.time.setText(self.elapsedTime.toString("hh:mm:ss"))


    def stopStopWatch(self):
        self.stopWatch.stop()


    def openModeWindow(self):
        if self.modeWindow:
            self.modeWindow.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())

