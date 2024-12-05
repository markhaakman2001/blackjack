# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

from PySide6.QtCore import Qt, QPropertyAnimation, QPoint

"""PySide6 port of the widgets/layouts/basiclayout example from Qt v5.x"""

import sys

from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QFrame, QWidget, QMainWindow, )


class Slots(QMainWindow):
    num_grid_rows = 3

    def __init__(self):
        super().__init__()

        self.create_grid_group_box()
        self.setCentralWidget(self._grid_group_box)
        self.setWindowTitle("SLOTS")
        self.showMaximized()

    def create_grid_group_box(self):

        self._grid_group_box = QGroupBox("Grid layout")
        layout = QGridLayout()

        for i in range(Slots.num_grid_rows):
            for j in range(3):

                placeHolder = QLabel("SIMPLESLOTHOLDER")
                placeHolder.setAlignment(Qt.AlignmentFlag.AlignCenter)
                placeHolder.setFrameStyle(QFrame.Panel)
                layout.addWidget(placeHolder, i, j)
                anim = QPropertyAnimation(placeHolder,b"pos")
                anim.setDuration(1000)
                anim.setStartValue(QPoint(0, 0))
                anim.setEndValue(QPoint(100, 250))
                anim.start()

        self._grid_group_box.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    slots = Slots()
    slots.show()
    sys.exit(app.exec())