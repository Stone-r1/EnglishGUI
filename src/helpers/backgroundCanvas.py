from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QLinearGradient, QRadialGradient
import sys


class BackgroundCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.UI()


    def UI(self):
        self.setFixedSize(400, 450)
        self.setWindowTitle("CANVAS")


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) 
        painter.setPen(Qt.GlobalColor.transparent)

        # background
        gradient = QLinearGradient(QPointF(self.width(), 0), QPointF(0, self.height()))
        gradient.setColorAt(1, QColor("#388087"))
        gradient.setColorAt(0, QColor("#6FB3B8"))

        brush = QBrush(gradient)
        painter.setBrush(brush)
        painter.drawRect(0, 0, self.width(), self.height())

        # big circle
        circle = QRadialGradient(QPointF(0, 0), 500)
        circle.setColorAt(1, QColor(185, 248, 255, 120))
        circle.setColorAt(0, QColor("#C2EDCE"))

        brush = QBrush(circle)
        painter.setBrush(brush)
        painter.drawEllipse(self.width() - 700, self.height() - 350, 500, 500)

        radialGradient = QRadialGradient(QPointF(self.width() - 30, 30), 100)
        radialGradient.setColorAt(0, QColor("#F6F6F2")) 
        radialGradient.setColorAt(1, QColor("#B9F8FF")) 

        brush = QBrush(radialGradient)
        painter.setBrush(brush)

        painter.drawEllipse(self.width() - 100, 30, 80, 80)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    canvas = BackgroundCanvas()
    canvas.show()
    sys.exit(app.exec())
