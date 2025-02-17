from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QCompleter, QComboBox, QStyledItemDelegate, QStyle, QFrame, QScrollArea, QGridLayout, QGraphicsBlurEffect
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QKeyEvent
import sys, subprocess, json

from helpers.backgroundCanvas import BackgroundCanvas


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

        wordLabel = QLabel(f"<b>{self.word}</b>", self)
        wordLabel.setFixedSize(320, 40)

        definitionLabel = QLabel(self.definition, self)
        definitionLabel.setWordWrap(True)
        definitionLabel.setFixedSize(320, 120)
        definitionLabel.setStyleSheet("font-size: 20px;")
        definitionLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
    
        layout.addWidget(wordLabel)
        layout.addWidget(definitionLabel)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setObjectName("Layout")

        self.setLayout(layout)
        self.setFixedSize(330, 160)

        self.setStyleSheet(""" 
            #Layout {
                border: 5px solid black;
                border-radius: 5px;
            } 
        """)

  

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


class ContentWindow(QWidget):
    def __init__(self, mainWindow=None):
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

        self.wordCompleter = QCompleter(self)
        self.wordInput.setCompleter(self.wordCompleter)

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
        self.categoryList.append("ALL")
        self.categoryList += json.loads(c.stdout)

        for i in self.categoryList:
            self.categoryInput.addItem(i)

        self.categoryInput.setCurrentIndex(0)

    
    def checkValidity(self): 
        category = self.wordInput.text()

        # temporary
        if category in self.categoryList:
            self.wordInput.setStyleSheet("background-color: green;")
        else:
            self.wordInput.setStyleSheet("background-color: red;") 


    def onCategorySelected(self, index):
        selectedCategory = self.categoryInput.itemText(index)
        self.result = subprocess.run([sys.executable, "db/words.py", "1", "2", selectedCategory, "4", "GETWORDS"], capture_output=True, text=True)
        
        self.results.clear()
        self.results = json.loads(self.result.stdout)

        for i in reversed(range(self.wordContainerLayout.count())): 
            widget = self.wordContainerLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # for later use
        for word, definition in self.results.items():
            wordDefWidget = WordDefinitionWidget(word, definition)
            self.wordContainerLayout.addWidget(wordDefWidget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContentWindow()
    window.show()
    sys.exit(app.exec())

