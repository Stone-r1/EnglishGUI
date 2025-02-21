from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPointF, QSize
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient

import sys

from startPage import StartWindow
from helpers.backgroundCanvas import BackgroundCanvas
from helpers.rgbSliderWidget import RGBSlider
from helpers.RGBSliderStyleSheet import RgbSliderStyleSheet
from helpers.moonButtonWidget import GradientButton
from helpers.escapeFunction import EscapeHandler

# TODO : add categories for changeable colors and saving to userColors.json

class SettingsWindow(QWidget, EscapeHandler):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
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


    def openMainWindow(self):
        if self.mainWindow:
            self.mainWindow.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    settingsWindow = SettingsWindow()
    settingsWindow.show()
    sys.exit(app.exec())
