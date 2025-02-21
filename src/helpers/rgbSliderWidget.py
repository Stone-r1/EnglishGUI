from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QSlider, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QColor, qRgb, QFont, QPixmap, QKeyEvent

import sys


class CustomLineEdit(QLineEdit):
    def __init__(self, parent = None, checkValidity = None): 
        super().__init__(parent)
        self.checkValidity = checkValidity

    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            event.accept()

            if self.checkValidity is not None:
                self.checkValidity()

            return
        super().keyPressEvent(event)


class RGBSlider(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.UI()


    def UI(self):
        self.setWindowTitle("RGB Slider")

        self.currentVal = QColor()
        self.colorDisplay = QImage(100, 100, QImage.Format.Format_ARGB32)
        self.colorDisplay.fill(Qt.GlobalColor.black)

        # for the future: add comparison between default color and user's color
        self.cdLabel = QLabel()
        self.cdLabel.setPixmap(QPixmap.fromImage(self.colorDisplay))
        self.cdLabel.setScaledContents(True)
        self.cdLabel.setStyleSheet("border: 2px solid black; border-radius: 5px;")
        self.cdLabel.setFixedSize(200, 100)

        # ============ red ==================
        redLabel = QLabel("Red")
        self.redSlider = QSlider(Qt.Orientation.Horizontal)
        self.redSlider.setObjectName("Red")
        self.redSlider.setMaximum(255)
        # ===================================

        # ========= green ===================
        greenLabel = QLabel("Green")
        self.greenSlider = QSlider(Qt.Orientation.Horizontal)
        self.greenSlider.setObjectName("Green")
        self.greenSlider.setMaximum(255)
        # ===================================

        # ======== blue =====================
        blueLabel = QLabel("Blue")
        self.blueSlider = QSlider(Qt.Orientation.Horizontal)
        self.blueSlider.setObjectName("Blue")
        self.blueSlider.setMaximum(255)
        # ===================================

        # ======== alpha ====================
        alphaLabel = QLabel("Alpha")
        self.alphaSlider = QSlider(Qt.Orientation.Horizontal)
        self.alphaSlider.setObjectName("Alpha")
        self.alphaSlider.setMaximum(255)
        self.alphaSlider.setValue(255) # default
        # ===================================

        self.rgbValueLineEdit = CustomLineEdit(self, self.checkValidity)
        self.rgbValueLineEdit.setPlaceholderText("Enter RGBA value")
        self.rgbValueLineEdit.setFixedSize(205, 35)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(redLabel, 0, 0, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.redSlider, 1, 0)

        grid.addWidget(greenLabel, 2, 0, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.greenSlider, 3, 0)

        grid.addWidget(blueLabel, 4, 0, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.blueSlider, 5, 0)

        grid.addWidget(alphaLabel, 6, 0, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.alphaSlider, 7, 0)


        self.redSlider.valueChanged.connect(self.checkValidity)
        self.greenSlider.valueChanged.connect(self.checkValidity)
        self.blueSlider.valueChanged.connect(self.checkValidity)
        self.alphaSlider.valueChanged.connect(self.checkValidity)

        # main container
        rgbWidget = QWidget()
        rgbWidget.setLayout(grid)

        verticalLayout = QVBoxLayout()
        verticalLayout.addWidget(self.cdLabel)
        verticalLayout.addWidget(rgbWidget)
        verticalLayout.setSpacing(10)
        verticalLayout.addWidget(self.rgbValueLineEdit)
        self.setLayout(verticalLayout)



    def updateRedSlider(self, value):
        self.redSlider.setValue(value)
        self.redValue(value)
        

    def updateGreenSlider(self, value):
        self.greenSlider.setValue(value)
        self.greenValue(value)


    def updateBlueSlider(self, value):
        self.blueSlider.setValue(value)
        self.blueValue(value)


    def updateAlphaSlider(self, value):
        self.alphaSlider.setValue(value)
        self.alphaValue(value)


    def checkValidity(self):
        sender = self.sender()

        if isinstance(sender, QSlider):
            self.rgbValueLineEdit.setText(", ".join(map(str, [self.redSlider.value(), self.greenSlider.value(),
                                                              self.blueSlider.value(), self.alphaSlider.value()])))
            self.rgbValueLineEdit.setStyleSheet("")

        else:
            text = self.rgbValueLineEdit.text().strip()
            parts = text.split(',')
            if len(parts) not in (3, 4):
                self.rgbValueLineEdit.setStyleSheet("background-color: pink;")
                return

            try:
                values = [int(part.strip()) for part in parts]
            except ValueError:
                self.rgbValueLineEdit.setStyleSheet("background-color: pink;")
                return

            if not all(0 <= channel <= 255 for channel in values):
                self.rgbValueLineEdit.setStyleSheet("background-color: pink;")
                return

            if (len(values) == 3):
                r, g, b = values
                a = 255

            else:
                r, g, b, a = values

            self.redSlider.setValue(r)
            self.greenSlider.setValue(g)
            self.blueSlider.setValue(b)
            self.alphaSlider.setValue(a)
            self.rgbValueLineEdit.setStyleSheet("")

        self.updateColorInfo(QColor(self.redSlider.value(), self.greenSlider.value(),
                                    self.blueSlider.value(), self.alphaSlider.value()))

    
    def updateColorInfo(self, color):
        self.currentVal = color
        self.colorDisplay.fill(color)
        self.cdLabel.setPixmap(QPixmap.fromImage(self.colorDisplay))


    def redValue(self, value):
        r = value
        g = self.greenSlider.value()
        b = self.blueSlider.value() 
        a = self.alphaSlider.value()
        newColor = QColor(r, g, b, a)
        self.updateColorInfo(newColor)


    def greenValue(self, value):
        r = self.redSlider.value()
        g = value
        b = self.blueSlider.value()
        a = self.alphaSlider.value()
        newColor = QColor(r, g, b, a)
        self.updateColorInfo(newColor)


    def blueValue(self, value):
        r = self.redSlider.value()
        g = self.greenSlider.value()
        b = value
        a = self.alphaSlider.value()
        newColor = QColor(r, g, b, a)
        self.updateColorInfo(newColor)


    def alphaValue(self, value):
        r = self.redSlider.value()
        g = self.greenSlider.value()
        b = self.blueSlider.value()
        a = value
        newColor = QColor(r, g, b, a)
        self.updateColorInfo(newColor)


    def getCurrentRGB(self):
        return self.rgbValueLineEdit.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(RgbSliderStyleSheet)
    rgbSlider = RGBSlider()
    rgbSlider.show()
    sys.exit(app.exec())
