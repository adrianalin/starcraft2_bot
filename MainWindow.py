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

        self.ui.maxNexusesSpinBox.valueChanged.connect(self.set_max_nexuses)
        self.ui.maxNexusesSpinBox.setValue(self.bot.max_nexuses)
        self.ui.maxNexusesSpinBox.setMinimum(1)
        self.ui.maxNexusesSpinBox.setMaximum(6)

        self.ui.maxStargatesSpinBox.valueChanged.connect(self.set_max_stargates)
        self.ui.maxStargatesSpinBox.setValue(self.bot.max_stargetes)
        self.ui.maxStargatesSpinBox.setMinimum(1)
        self.ui.maxStargatesSpinBox.setMaximum(6)

    def update_picture(self):
        flipped = self.bot.flipped
        qimage = QImage(flipped, flipped.shape[1], flipped.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(self.ui.pictureLabel.width(), self.ui.pictureLabel.height(), Qt.KeepAspectRatio)
        self.ui.pictureLabel.setPixmap(pixmap)

    def update_units(self):
        units_effective = self.bot.units_effective()
        if self.ui.unitsEffectiveLayout.rowCount() != len(units_effective):
            for index in range(self.ui.unitsEffectiveLayout.count()):
                self.ui.unitsEffectiveLayout.removeRow(0)

            for (unit_type, count_ready, count_not_ready) in units_effective:
                self.ui.unitsEffectiveLayout.addRow(str(unit_type).split('.')[1],
                                                    QLabel(str(count_ready) + ' + ' + str(count_not_ready), self))

        if self.ui.unitsEffectiveLayout.rowCount() == len(units_effective):
            for index, (unit_type, count_ready, count_not_ready) in enumerate(units_effective):
                self.ui.unitsEffectiveLayout.itemAt(index, QFormLayout.LabelRole).widget().\
                    setText(str(unit_type).split('.')[1])
                self.ui.unitsEffectiveLayout.itemAt(index, QFormLayout.FieldRole).widget().\
                    setText(str(count_ready) + ' + ' + str(count_not_ready))

        self.ui.action_label.setText(self.bot.attack_choice())
        self.ui.game_time_label.setText(str(int(self.bot.game_time)))

    def set_max_nexuses(self, count):
        self.bot.set_max_nexuses(count)

    def set_max_stargates(self, count):
        self.bot.set_max_stargates(count)

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
