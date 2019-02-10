from PySide2.QtWidgets import QMainWindow, QMessageBox, QApplication, QLabel, QFormLayout
from PySide2.QtCore import Qt, Signal, QTimer
from PySide2.QtGui import QCloseEvent, QImage, QPixmap

from ui_MainWindow import Ui_MainWindow

from sc2_bot import BotTest


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.bot = BotTest()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Sc2 bot')

        timer = QTimer(self)
        timer.timeout.connect(self.update_picture)
        timer.timeout.connect(self.update_units)
        timer.start(50)

    def update_picture(self):
        flipped = self.bot.flipped
        qimage = QImage(flipped, flipped.shape[1], flipped.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(self.ui.pictureLabel.width(), self.ui.pictureLabel.height(), Qt.KeepAspectRatio)
        self.ui.pictureLabel.setPixmap(pixmap)

    def update_units(self):
        if self.ui.unitsEffectiveLayout.rowCount() == 0:
            for unit_type, count in self.bot.units_effective().items():
                self.ui.unitsEffectiveLayout.addRow(str(unit_type).split('.')[1], QLabel(str(count), self))

        for index, unit_type in enumerate(self.bot.units_effective()):
            self.ui.unitsEffectiveLayout.itemAt(index, QFormLayout.LabelRole).widget().\
                setText(str(unit_type).split('.')[1])
            self.ui.unitsEffectiveLayout.itemAt(index, QFormLayout.FieldRole).widget().\
                setText(str(self.bot.units_effective()[unit_type]))

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
