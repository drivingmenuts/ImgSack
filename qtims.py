#!/usr/bin/env python3

import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QStatusBar,
    QVBoxLayout,
    QWidget
)


class LabelSet(QWidget):
    def __init__(self, label: str, buttons: list = ('-' * 9), parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        layout.addWidget(QLabel(label))

        if len(buttons) < 9:
            buttons.append('-' * (9 - len(buttons)))

        for button_text in buttons:
            button = QPushButton(button_text)
            layout.addWidget(button)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ImgSack")
        self.resize(QSize(800, 600))

        main_layout = QHBoxLayout()
        main_layout.addWidget(QLabel("ImgSack"))

        no_modifier_widget = LabelSet("")
        alt_modifier_widget = LabelSet("Alt")
        ctrl_modifier_widget = LabelSet("Ctrl")
        shift_modifier_widget = LabelSet("Shift")

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
        right_column_layout.addWidget(label_key_layout)
        right_column_layout.addWidget(utility_keys_layout)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
