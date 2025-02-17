from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea,
    QFrame, QHBoxLayout, QPushButton, QGridLayout, QLineEdit, QCompleter, QMenu, QComboBox
)
from PyQt6.QtCore import Qt
import sys


class CustomComboBox(QComboBox):
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        # Get the currently selected item
        current_index = self.currentIndex()
        current_text = self.currentText()

        # Add selected item as the first action (disabled for visibility)
        selected_action = QAction(current_text, self)
        selected_action.setEnabled(False)  # Show as label, not selectable
        menu.addAction(selected_action)

        # Add a separator
        menu.addSeparator()

        # Add other items below the selected one
        for i in range(self.count()):
            if i != current_index:  # Exclude the currently selected one
                action = QAction(self.itemText(i), self)
                action.triggered.connect(lambda checked, index=i: self.setCurrentIndex(index))
                menu.addAction(action)

        # Show the context menu at the cursor position
        menu.exec_(event.globalPos())


class WordDefinitionWidget(QFrame):
    def __init__(self, word, definition, parent=None):
        super().__init__(parent)
        self.word = word
        self.definition = definition
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        wordLabel = QLabel(f"<b>{self.word}</b>", self)
        wordLabel.setFixedSize(100, 30)

        definitionLabel = QLabel(self.definition, self)
        definitionLabel.setWordWrap(True)
        definitionLabel.setFixedSize(320, 80)
    
        layout.addWidget(wordLabel, 0, 0, 1, 3)
        layout.addWidget(definitionLabel, 1, 0, 1, 3)

        self.setLayout(layout)

        self.setStyleSheet(""" 
            QFrame {
                border: 2px solid black;
                border-radius: 5px;
            } 
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

        combo = CustomComboBox()
        combo.addItems(["Option 1", "Option 2", "Option 3", "Option 4"])

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
        layout.addWidget(combo)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContentWindow()
    window.show()
    sys.exit(app.exec())

