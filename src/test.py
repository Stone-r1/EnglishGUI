from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea,
    QFrame, QHBoxLayout, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt
import sys

class WordDefinitionWidget(QFrame):
    def __init__(self, word, definition, parent=None):
        super().__init__(parent)
        self.word = word
        self.definition = definition
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        wordLabel = QLabel(f"<b>{self.word}</b>", self)
        wordLabel.setFixedSize(80, 80)

        definitionLabel = QLabel(self.definition, self)
        definitionLabel.setWordWrap(True)
        definitionLabel.setFixedSize(180, 80)
    
        layout.addWidget(wordLabel, 0, 0, 1, 1)
        layout.addWidget(definitionLabel, 0, 1, 1, 3)

        self.setLayout(layout)

        self.setStyleSheet(""" 
            QLabel {
                font-family: 'Arial', sans-serif;
                color: #333333;
            }
            QLabel::selection {
                background-color: #ffcc00;
                color: white;
            }
            QFrame:hover {
                background-color: #e6f7ff;
            }
        """)



class ContentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Words and Definitions")
        self.setFixedSize(400, 500)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Scroll Area Setup
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)

        # Create a container widget to hold all word-definition widgets
        containerWidget = QWidget()
        containerLayout = QVBoxLayout()

        # Sample data: word and definition pairs
        results = [
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long."),
            ("Word 3", "This is the definition of word 3."),
        ]

        # Add each word-definition pair to the container
        for word, definition in results:
            wordDefWidget = WordDefinitionWidget(word, definition)
            containerLayout.addWidget(wordDefWidget)

        containerWidget.setLayout(containerLayout)
        scrollArea.setWidget(containerWidget)

        layout.addWidget(scrollArea)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContentWindow()
    window.show()
    sys.exit(app.exec())

