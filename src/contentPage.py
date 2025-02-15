from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QCompleter, QComboBox, QStyledItemDelegate, QStyle
from PyQt6.QtCore import Qt, QStringListModel
import sys, subprocess, json

from helpers.backgroundCanvas import BackgroundCanvas

class ContentWindow(QWidget):
    def __init__(self, mainWindow=None):
        super().__init__()
        self.mainWindow = mainWindow
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

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter a category:"))
        layout.addWidget(self.categoryInput)
        self.setLayout(layout)


    def getCategories(self): 
        c = subprocess.run([sys.executable, "db/words.py", "1", "2", "3", "4", "GET"], capture_output=True, text=True)
        categoryList = json.loads(c.stdout)
        categoryList.append("All")

        model = QStringListModel(categoryList)
        self.categoriesCompleter.setModel(model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContentWindow()
    window.show()
    sys.exit(app.exec())

