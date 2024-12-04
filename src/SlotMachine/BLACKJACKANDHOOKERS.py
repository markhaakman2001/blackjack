# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtCore import QPropertyAnimation, QParallelAnimationGroup, QSequentialAnimationGroup, QRect, QSize
"""PySide6 port of the widgets/layouts/basiclayout example from Qt v5.x"""

import sys

from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QVBoxLayout, QFrame)


class Slots(QDialog):
    num_grid_rows = 5

    def __init__(self):
        super().__init__()

        self.create_grid_group_box()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self._grid_group_box)
        self.setLayout(main_layout)
        self.setWindowTitle("SLOTS")
        self.showMaximized()
        self.button = QPushButton("start")
        main_layout.addWidget(self.button)
        self.button.clicked.connect(self.start)

    def create_grid_group_box(self):
        self._grid_group_box = QGroupBox("Grid layout")
        layout = QGridLayout()
        self.animationgroup = QParallelAnimationGroup()

        for i in range(Slots.num_grid_rows):
            for j in range(6):
                placeHolder1 = QLabel("SIMPLESLOTHOLDER")
                placeHolder1.setAlignment(Qt.AlignmentFlag.AlignCenter)
                placeHolder1.setFrameStyle(QFrame.Panel)
                

                layout.addWidget(placeHolder1, i, j)

                anim1 = QPropertyAnimation(placeHolder1, b"geometry")
                anim1.setStartValue(QSize(0, 0))
                anim1.setEndValue(QSize(100, 100))
                anim1.setDuration(1500)
                self.animationgroup.addAnimation(anim1)

        self._grid_group_box.setLayout(layout)
        
    
    def start(self):
        self.animationgroup.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    slots = Slots()
    sys.exit(slots.exec())