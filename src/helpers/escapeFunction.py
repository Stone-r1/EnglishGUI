from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent


class EscapeHandler:
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            event.accept()
            self.openMainWindow()
        else:
            pass
