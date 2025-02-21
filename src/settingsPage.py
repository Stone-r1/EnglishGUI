from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget
from PyQt6.QtCore import Qt, QPointF, QSize
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient

import sys
import json

from startPage import StartWindow
from helpers.backgroundCanvas import BackgroundCanvas
from helpers.rgbSliderWidget import RGBSlider
from helpers.RGBSliderStyleSheet import RgbSliderStyleSheet
from helpers.moonButtonWidget import GradientButton
from helpers.escapeFunction import EscapeHandler


class SettingsWindow(QWidget, EscapeHandler):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.selectedItem = None
        self.baseCase = {} 
        self.UI()


    def UI(self): 
        self.setFixedSize(400, 450)
        self.setWindowTitle("GUI")

        self.background = BackgroundCanvas()
        self.background.setParent(self)
        self.background.lower()

        self.sliderWidget = RGBSlider(self)
        self.sliderWidget.setGeometry(0, 100, 220, 350)
        self.sliderWidget.setStyleSheet(RgbSliderStyleSheet)
        self.sliderWidget.raise_()

        settingsButton = GradientButton("+", self.background, self)
        settingsButton.setObjectName("SettingsButton")
        settingsButton.clicked.connect(self.openMainWindow)
        settingsButton.setGeometry(self.width() - 100, 30, 80, 80)
        settingsButton.raise_()

        self.returnButton = QPushButton("Return", self)
        self.returnButton.clicked.connect(self.openMainWindow)
        self.returnButton.setGeometry(10, 10, 145, 50)

        self.baseConfigButton = QPushButton("O", self)
        self.baseConfigButton.clicked.connect(self.returnBaseConfig)
        self.baseConfigButton.setGeometry(160, 10, 50, 50)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(220, 120, 170, 245)
        self.listWidget.addItems(["background0", "background1", "bigCircle0", 
                                  "bigCircle1", "smallCircle0", "smallCircle1"])
        self.listWidget.itemClicked.connect(self.selectItem)

        self.applyButton = QPushButton("Apply", self)
        self.applyButton.setGeometry(220, 380, 170, 60)
        self.applyButton.clicked.connect(self.applyColor)


    def selectItem(self, item):
        self.selectedItem = item.text()


    def applyColor(self):
        #if self.sliderWidget.checkValidity():
        color = self.sliderWidget.getCurrentRGB() # it's string
        print(f"{self.selectedItem}: {color}")
        self.updateUserJson(color)


    def updateUserJson(self, color):
        with open("helpers/userColors.json", "r") as data:
            self.baseCase.update(json.load(data))

        r, g, b, a = map(int, color.replace(" ", "").split(','))
        
        if self.selectedItem:
            self.baseCase[self.selectedItem] = [r, g, b, a]
            print(f"Updated {self.selectedItem}: {r}, {g}, {b}, {a}")

        with open("helpers/userColors.json", "w") as newData:
            json.dump(self.baseCase, newData, indent=4)


    def returnBaseConfig(self):
        with open("helpers/userColors.json", "w") as data:
            data.write("{\n}")


    def openMainWindow(self):
        if self.mainWindow:
            self.mainWindow.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settingsWindow = SettingsWindow()
    settingsWindow.show()
    sys.exit(app.exec())
