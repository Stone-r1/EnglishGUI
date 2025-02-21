from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QCompleter, QComboBox, QStyledItemDelegate, QStyle, QFrame, QScrollArea, QGridLayout, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QKeyEvent

import sys
import subprocess
import json

from helpers.backgroundCanvas import BackgroundCanvas
from helpers.mainPageStyleSheet import styleSheet
from helpers.escapeFunction import EscapeHandler


class CustomComboBox(QComboBox):
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        currentIndex = self.currentIndex()
        currentText = self.currentText()

        selectedAction = QAction(currentText, self)
        selectedAction.setEnabled(False) 
        menu.addAction(selectedAction)

        menu.addSeparator()

        for i in range(self.count()):
            if i != currentIndex:
                action = QAction(self.itemText(i), self)
                action.triggered.connect(lambda checked, index = i: self.setCurrentIndex(index))
                menu.addAction(action)
         
        menu.exec(event.globalPos())


class WordDefinitionWidget(QFrame):
    def __init__(self, word, definition, parent=None):
        super().__init__(parent)
        self.word = word
        self.definition = definition
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        blurOverlay = QWidget(self)
        blurOverlay.setGeometry(0, 0, 340, 165)
        blurOverlay.setStyleSheet("background-color: rgba(194, 237, 206, 0.5);")
        
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(30)
        blurOverlay.setGraphicsEffect(blur_effect)

        wordLabel = QLabel(f"<b>{self.word}</b>", self)
        wordLabel.setFixedSize(320, 45) 
        wordLabel.setStyleSheet("border: none; color: #253B56; font-size: 35px;")

        definitionLabel = QLabel(self.definition, self)
        definitionLabel.setWordWrap(True)
        definitionLabel.setFixedSize(320, 120)
        definitionLabel.setStyleSheet("font-size: 20px; border: none; color: #253B56;")
        definitionLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
    
        layout.addWidget(wordLabel)
        layout.addWidget(definitionLabel)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 0, 0, 0)

        self.setLayout(layout)
        self.setFixedSize(340, 165)

        self.setStyleSheet("border-radius: 10px; border: 2px solid #253B56;") 


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


class ContentWindow(QWidget, EscapeHandler):
    def __init__(self, mainWindow = None):
        super().__init__()
        self.mainWindow = mainWindow
        self.categoryList = []
        self.results = {}
        self.UI()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        self.categoryInput = CustomComboBox(self)
        self.categoryInput.setPlaceholderText("Type a category...")
        self.categoryInput.setFixedSize(190, 50)
        self.getCategories()
        self.categoryInput.currentIndexChanged.connect(self.onCategorySelected)

        self.wordInput = CustomLineEdit(checkValidity = self.checkValidity, parent = self)
        self.wordInput.setPlaceholderText("Type a Word...")
        self.wordInput.setStyleSheet("font-size: 20px;")
        self.wordInput.setFixedSize(180, 50)
        self.wordInput.textChanged.connect(self.onWordInputChanged)

        wordContainerWidget = QWidget()
        self.wordContainerLayout = QVBoxLayout()
        
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
            
        wordContainerWidget.setLayout(self.wordContainerLayout)
        scrollArea.setWidget(wordContainerWidget)

        layout = QGridLayout()
        layout.addWidget(scrollArea, 0, 0, 4, 4)
        layout.addWidget(self.categoryInput, 4, 0, 1, 2)
        layout.addWidget(self.wordInput, 4, 2, 1, 2)

        self.setLayout(layout)


    def getCategories(self): 
        c = subprocess.run([sys.executable, "db/words.py", "1", "2", "3", "4", "GET"], capture_output=True, text=True)
        if "ALL" not in json.loads(c.stdout):
            self.categoryList.append("ALL")
        self.categoryList += json.loads(c.stdout)

        for i in self.categoryList:
            self.categoryInput.addItem(i)

        self.categoryInput.setCurrentIndex(0) 


    def onCategorySelected(self, index):
        selectedCategory = self.categoryInput.itemText(index)
        self.result = subprocess.run([sys.executable, "db/words.py", "1", "2", selectedCategory, "4", "GETWORDS"], capture_output=True, text=True)
        
        self.results.clear()
        self.results = json.loads(self.result.stdout)

        for i in reversed(range(self.wordContainerLayout.count())): 
            widget = self.wordContainerLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for word, definition in self.results.items():
            wordDefWidget = WordDefinitionWidget(word, definition)
            self.wordContainerLayout.addWidget(wordDefWidget)
        
        # add words to completer only after getting words from particular category
        self.wordCompleter = QCompleter(self)
        wordListModel = QStringListModel(list(self.results.keys()))
        self.wordCompleter.setModel(wordListModel)
        self.wordInput.setCompleter(self.wordCompleter)

        self.wordCompleter.activated.connect(self.onWordSelected)


    def onWordSelected(self, selectedWord):
        self.wordInput.setText(selectedWord)
        self.modifyWindowWords()


    def onWordInputChanged(self):
        text = self.wordInput.text().strip()

        if not text:
            self.restoreWords()
            return

        self.modifyWindowWords()


    def restoreWords(self):
        # restore all words when input is cleared
        for i in reversed(range(self.wordContainerLayout.count())): 
            widget = self.wordContainerLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for word, definition in self.results.items():
            wordDefWidget = WordDefinitionWidget(word, definition)
            self.wordContainerLayout.addWidget(wordDefWidget)


    def modifyWindowWords(self): 
        selectedWord = self.wordInput.text().strip()
        matchingWords = {word: definition for word, definition in self.results.items() if selectedWord in word}
        
        for i in reversed(range(self.wordContainerLayout.count())):
            widget = self.wordContainerLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for word, definition in matchingWords.items():
            wordDefWidget = WordDefinitionWidget(word, definition)
            self.wordContainerLayout.addWidget(wordDefWidget)


    def checkValidity(self): 
        self.onWordInputChanged()


    def openMainWindow(self):
        if self.mainWindow:
            self.mainWindow.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContentWindow()
    window.show()
    sys.exit(app.exec())
