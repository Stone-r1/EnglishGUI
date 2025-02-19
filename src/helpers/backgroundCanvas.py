from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsBlurEffect, QPushButton
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient, QPixmap
import sys
import json

# TODO : maybe I'll have to add one more function that will open the window again after pressing one button on the main page

class BackgroundCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.colorsDict = {}
        self.loadColors()
        self.UI()


    def loadColors(self):
        self.colorsDict = self.parseDefaultColors()
        self.colorsDict.update(self.parseUserColors())


    def parseDefaultColors(self):
        with open("helpers/defaultColors.json", "r") as defaultData:
            defaultColors = json.load(defaultData)

        return defaultColors


    def parseUserColors(self):
        with open("helpers/userColors.json", "r") as userData:
            userColors = json.load(userData)

        return userColors


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("CANVAS")


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) 
        painter.setPen(Qt.GlobalColor.transparent)

        # background
        gradient = QLinearGradient(QPointF(self.width(), 0), QPointF(0, self.height())) 
        gradient.setColorAt(1, QColor(self.colorsDict["background1"][0], self.colorsDict["background1"][1],
                                      self.colorsDict["background1"][2], self.colorsDict["background1"][3]))
        gradient.setColorAt(0, QColor(self.colorsDict["background0"][0], self.colorsDict["background0"][1],
                                      self.colorsDict["background0"][2], self.colorsDict["background0"][3]))

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.drawRect(0, 0, self.width(), self.height())

        # big circle
        bigCircle = QRadialGradient(QPointF(0, 0), 500)
        bigCircle.setColorAt(1, QColor(self.colorsDict["bigCircle1"][0], self.colorsDict["bigCircle1"][1],
                                       self.colorsDict["bigCircle1"][2], self.colorsDict["bigCircle1"][3]))
        bigCircle.setColorAt(0, QColor(self.colorsDict["bigCircle0"][0], self.colorsDict["bigCircle0"][1],
                                       self.colorsDict["bigCircle0"][2], self.colorsDict["bigCircle0"][3]))

        brush = QBrush(bigCircle)
        painter.setBrush(brush)
        painter.drawEllipse(self.width() - 700, self.height() - 350, 500, 500)

        # small circle
        smallCircle = QRadialGradient(QPointF(self.width() - 30, 30), 100)
        smallCircle.setColorAt(0, QColor(self.colorsDict["smallCircle0"][0], self.colorsDict["smallCircle0"][1],
                                         self.colorsDict["smallCircle0"][2], self.colorsDict["smallCircle0"][3]))  
        smallCircle.setColorAt(1, QColor(self.colorsDict["smallCircle1"][0], self.colorsDict["smallCircle1"][1],
                                         self.colorsDict["smallCircle1"][2], self.colorsDict["smallCircle1"][3]))

        brush = QBrush(smallCircle)
        painter.setBrush(brush)
        painter.drawEllipse(self.width() - 100, 30, 80, 80)

        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    canvas = BackgroundCanvas()
    canvas.show()
    sys.exit(app.exec())
