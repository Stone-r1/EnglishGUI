from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsBlurEffect, QPushButton
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QPixmap
import sys


class GradientButton(QPushButton):
    def __init__(self, text, background, parent = None):
        super().__init__(text, parent)
        self.background = background

    
    def paintEvent(self, event): 

        painter = QPainter(self) 
        gradient = QRadialGradient(QPointF(self.width() - 30, 30), 100)
        gradient.setColorAt(0, QColor(self.background.colorsDict["smallCircle0"][0],
                                      self.background.colorsDict["smallCircle0"][1],
                                      self.background.colorsDict["smallCircle0"][2],
                                      self.background.colorsDict["smallCircle0"][3]))

        gradient.setColorAt(1, QColor(self.background.colorsDict["smallCircle1"][0],
                                      self.background.colorsDict["smallCircle1"][1],
                                      self.background.colorsDict["smallCircle1"][2],
                                      self.background.colorsDict["smallCircle1"][3]))

        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen) 
        painter.drawEllipse(self.rect())
        
        super().paintEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    button = GradientButton()
    button.show()
    sys.exit(app.exec())
