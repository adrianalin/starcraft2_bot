from PySide2.QtWidgets import QMainWindow, QMessageBox, QApplication
from PySide2.QtCore import Qt, Signal, QTimer
from PySide2.QtGui import QCloseEvent, QImage, QPixmap

from ui_MainWindow import Ui_MainWindow

from sc2_bot import BotTest


class MainWindow(QMainWindow):
    bot = BotTest()

    def __init__(self):
        super(MainWindow, self).__init__()

        timer = QTimer(self)
        timer.timeout.connect(self.update_picture)
        timer.start(50)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Sc2 bot')
        self.ui.horizontalSlider.setTickInterval(1)
        self.ui.horizontalSlider.valueChanged.connect(self.sliderChanged)

    def sliderChanged(self, val):
        print('val: %d' % (val))

    def update_picture(self):
        flipped = self.bot.flipped
        qimage = QImage(flipped, flipped.shape[1], flipped.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(self.ui.pictureLabel.width(), self.ui.pictureLabel.height(), Qt.KeepAspectRatio)
        self.ui.pictureLabel.setPixmap(pixmap)

    def closeEvent(self, event: QCloseEvent):
        ret = QMessageBox.question(self, self.tr("Sc2 bot"),
                                  self.tr("Are you sure you want to exit?"),
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ret == QMessageBox.Yes:
            event.accept()
            self.bot.stop_game()
        else:
            event.ignore()

    @property
    def getbot(self):
        return self.bot
