#!/usr/bin/env python3

import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QStatusBar,
    QVBoxLayout,
    QWidget
)

DEBUG = True


class LabelSetWidget(QFrame):
    def __init__(self, label: str, buttons: list = ('-' * 9), parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        title_label = QLabel(label)
        title_label.setMinimumWidth(512)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        if len(buttons) < 9:
            buttons.append('-' * (9 - len(buttons)))

        for button_text in buttons:
            button = QPushButton(button_text)
            layout.addWidget(button)

        if DEBUG:
            self.setFrameShape(self.Shape.Box)
            # pass

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ImgSack")

        main_layout = QHBoxLayout()

        image_label = QLabel("Image")
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setMinimumWidth(768)
        image_label.setMinimumHeight(768)
        main_layout.addWidget(image_label)

        no_modifier_widget = LabelSetWidget("None")
        alt_modifier_widget = LabelSetWidget("Alt")
        ctrl_modifier_widget = LabelSetWidget("Ctrl")
        shift_modifier_widget = LabelSetWidget("Shift")

        label_key_layout = QStackedLayout()
        label_key_layout.addWidget(no_modifier_widget)
        label_key_layout.addWidget(alt_modifier_widget)
        label_key_layout.addWidget(ctrl_modifier_widget)
        label_key_layout.addWidget(shift_modifier_widget)

        utility_keys_layout = QHBoxLayout()
        skip_button_0 = QPushButton("0 - Skip")
        trash_button_decimal = QPushButton(". - Trash")

        utility_keys_layout.addWidget(skip_button_0)
        utility_keys_layout.addWidget(trash_button_decimal)

        right_column_layout = QVBoxLayout()
        right_column_layout.addLayout(label_key_layout)
        right_column_layout.addLayout(utility_keys_layout)

        main_layout.addLayout(right_column_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
