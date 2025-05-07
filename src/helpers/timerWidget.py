from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QTimer, QTime, pyqtSignal, Qt


class TimerWidget(QLabel):
    finished = pyqtSignal()
    tick = pyqtSignal(QTime)

    def __init__(self, mode = "STOPWATCH", startTime = None, countdownStart = 5, parent = None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("font-size: 24px;")

        self.mode = mode
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)

        if mode == 'STOPWATCH':
            self.elapsedTime = QTime(0, 0, 0)
        elif mode == 'COUNTDOWN':
            self.countdownTime = countdownStart
            self.setStyleSheet("font-size: 16px;")
            self.setText(f"Starting in {self.countdownTime}...")

        if startTime:
            self.elapsedTime = startTime

    def start(self):
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def updateTime(self):
        if self.mode == 'STOPWATCH':
            self.elapsedTime = self.elapsedTime.addSecs(1)
            self.setText(self.elapsedTime.toString("hh:mm:ss"))
            self.tick.emit(self.elapsedTime)

        elif self.mode == 'COUNTDOWN':
            if self.countdownTime > 0:
                self.setText(f"Starting in {self.countdownTime}...")
                self.countdownTime -= 1
            else:
                self.timer.stop()
                self.finished.emit()
