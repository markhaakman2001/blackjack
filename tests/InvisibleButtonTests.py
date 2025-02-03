from PySide6 import QtWidgets
from PySide6.QtWidgets import QPushButton, QComboBox, QDialog, QCheckBox
from PySide6.QtWidgets import QStyleOption, QStyle, QStyleOptionButton
from PySide6.QtCore import Slot, QObject, Signal, QPropertyAnimation, QPoint, QEasingCurve, QSize, Qt
import PySide6.QtCore as Core
from PySide6.QtCore import QRect, QPropertyAnimation, Property, QParallelAnimationGroup, QSequentialAnimationGroup, QAbstractAnimation, QRectF
from PySide6.QtGui import QImageReader, QImage, QPixmap, QPicture, QPainter, QBrush, QColor, Qt, QRegion, QIcon
from src.CustomUIfiles.backgroundwidget import BaccaratBackground
import sys



class InvisibleButtonWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.c_widget = BaccaratBackground()
        self.setCentralWidget(self.c_widget)
        self.c_widget.resize(QSize(1200, 600))
        self.resize(1200, 700)
        self.custom_widget = CustomGraphics()
        self.custom_widget.setParent(self)


class CustomRect(QRect):

    def __init__(self):
        self.topLeft  = QPoint(50, 50)
        self.topRight = QPoint(400, 400)
        super().__init__(self.topLeft, self.topRight)
        print(self.isValid())

class CustomGraphics(QtWidgets.QGraphicsWidget):

    def __init__(self):
        super().__init__()
        self.resize(QSize(100, 100))


def main():
    app = QtWidgets.QApplication(sys.argv)
    ui = InvisibleButtonWindow()
    ui.show()
    app.exec()


if __name__ == "__main__":
    main()