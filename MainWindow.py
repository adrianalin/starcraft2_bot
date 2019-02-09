from PySide2.QtWidgets import QMainWindow, QMessageBox, QApplication
from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QCloseEvent

from ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow):
    exit_signal = Signal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Sc2 bot')
        self.ui.horizontalSlider.setTickInterval(1)
        self.ui.horizontalSlider.valueChanged.connect(self.sliderChanged)

    def sliderChanged(self, val):
        print('val: %d' % (val))

    def update_picture(self, pixmap):
        pixmap = pixmap.scaled(self.ui.videoLabel.width(), self.ui.videoLabel.height(), Qt.KeepAspectRatio)
        self.ui.videoLabel.setPixmap(pixmap)

    def closeEvent(self, event: QCloseEvent):
        ret = QMessageBox.question(self, self.tr("Sc2 bot"),
                                  self.tr("Are you sure you want to exit?"),
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.exit_signal.emit()
            event.accept()
        else:
            event.ignore()
