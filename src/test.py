from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QHBoxLayout
from PyQt6.QtCore import Qt
import sys

class WordDefinitionWidget(QFrame):
    def __init__(self, word, definition, parent=None):
        super().__init__(parent)
        self.word = word
        self.definition = definition
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        
        # Word label
        wordLabel = QLabel(f"<b>{self.word}</b>", self)
        wordLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Definition label
        definitionLabel = QLabel(self.definition, self)
        definitionLabel.setWordWrap(True)
        definitionLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Adding word and definition to the layout
        layout.addWidget(wordLabel)
        layout.addWidget(definitionLabel)

        self.setLayout(layout)

        self.setFixedSize(330, 80)


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
            ("Word 1", "This is the definition of word . the definition of word "),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3. the definition of word "),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),

            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),
            
            ("Word 1", "This is the definition of word 1."),
            ("Word 2", "This is the definition of word 2, which is quite long and may need scrolling."),
            ("Word 3", "This is the definition of word 3."),


        ]

        # Add each word-definition pair to the container
        for word, definition in results:
            wordDefWidget = WordDefinitionWidget(word, definition)
            containerLayout.addWidget(wordDefWidget)

        # Set the layout of the container and the scroll area
        containerWidget.setLayout(containerLayout)
        scrollArea.setWidget(containerWidget)

        # Add scroll area to the main layout
        layout.addWidget(scrollArea)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ContentWindow()
    window.show()
    sys.exit(app.exec())

