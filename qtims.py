#!/usr/bin/env python3

PROGRAM_NAME = 'ImageSack'
PROGRAM_VERSION = '0.0.1rNone'
PYTHON_VERSION = '3.9'
VERSION_INFO = f'{PROGRAM_NAME} v{PROGRAM_VERSION} - {PYTHON_VERSION}'

import qtkeymapper

import argparse
import logging
import json
import os
import sys

from pathlib import Path
from rich.logging import RichHandler

logging.basicConfig(level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)

logging.info(f'{VERSION_INFO} started')

NO_ALBUM_MESSAGE = 'No albums defined'
DEFAULT_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.webp', '.svg']
MAX_ALBUMS = 36  # no mod, shift, alt, ctrl * 9 (on the numeric keypad)

from PySide6.QtCore import *
from PySide6.QtWidgets import *

DEBUG = True


class LabelSetWidget(QFrame):
    def __init__(self, label: str, buttons=None, parent=None):
        super().__init__(parent)
        if buttons is None:
            buttons = []
        layout = QVBoxLayout()

        title_label = QLabel(label)
        title_label.setMinimumWidth(384)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        for button_text in buttons:
            button = QPushButton(button_text)
            layout.addWidget(button)

        if len(buttons) < 9:
            for _i in range(9 - len(buttons)):
                button = QPushButton(NO_ALBUM_MESSAGE)
                layout.addWidget(button)

        if DEBUG:
            logger.debug(r'Adding frame')
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

        self.keyPressEventFilter = KeyPressEventFilter(self)
        self.installEventFilter(self.keyPressEventFilter)


class KeyPressEventFilter(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            logger.info(f'key_press: {event.key()}')
        return False


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
