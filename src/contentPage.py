from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QCompleter, QComboBox, QStyledItemDelegate, QStyle
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QKeyEvent
import sys, subprocess, json

from helpers.backgroundCanvas import BackgroundCanvas


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
        self.UI()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        self.categoryInput = QLineEdit(self)
        self.categoryInput.setPlaceholderText("Type a category...")

        self.categoriesCompleter = QCompleter(self)
        self.categoryInput.setCompleter(self.categoriesCompleter)
        self.getCategories()

        self.wordInput = CustomLineEdit(checkValidity = self.checkValidity, parent = self)
        self.wordInput.setPlaceholderText("Type a Word...")

        self.wordCompleter = QCompleter(self)
        self.wordInput.setCompleter(self.wordCompleter)

        layout = QVBoxLayout()
        layout.addWidget(self.categoryInput)
        layout.addWidget(self.wordInput)
        self.setLayout(layout)


    def getCategories(self): 
        c = subprocess.run([sys.executable, "db/words.py", "1", "2", "3", "4", "GET"], capture_output=True, text=True)
        self.categoryList = json.loads(c.stdout)
        self.categoryList.append("All")

        model = QStringListModel(self.categoryList)
        self.categoriesCompleter.setModel(model)


    def checkValidity(self): 
        category = self.wordInput.text()
        
        if category in self.categoryList:
            self.wordInput.setStyleSheet("background-color: green;")
        else:
            self.wordInput.setStyleSheet("background-color: red;") 



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContentWindow()
    window.show()
    sys.exit(app.exec())

