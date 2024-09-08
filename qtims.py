#!/usr/bin/env python3

PROGRAM_NAME = "ImageSack"
PROGRAM_VERSION = "0.0.1rNone"
PYTHON_VERSION = "3.9"
VERSION_INFO = f"{PROGRAM_NAME} v{PROGRAM_VERSION} - {PYTHON_VERSION}"

import argparse
import logging
import json
import os
import sys

from enum import Enum
from pathlib import Path
from rich.logging import RichHandler

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)

logging.info(f"{VERSION_INFO} started")

NO_ALBUM_MESSAGE = "No album defined"
DEFAULT_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
    ".svg",
]
MAX_ALBUMS = 36  # no mod, shift, alt, ctrl * 9 (on the numeric keypad)


class FontSize(Enum):
    TITLE = 24
    SUBTITLE = 20
    NORMAL = 16
    SMALL = 12
    TINY = 10


# QT swaps key names for modifiers on MacOS. This switches them back.
MODIFIER_KEYS = ["", "Shift", "Ctrl", "Alt"]
KEYPRESS_VALUES = [-1, 16777248, 16777250, 16777251]
DEBUG = True
RIGHT_COLUMN_WIDTH = 384


class LabelSetWidget(QFrame):
    def __init__(self, title: str, buttons=None, parent=None):
        super().__init__(parent)
        if buttons is None:
            buttons = []
        layout = QVBoxLayout()

        title_label = QLabel(title)
        title_label.setMinimumWidth(RIGHT_COLUMN_WIDTH)
        title_label.setMaximumWidth(RIGHT_COLUMN_WIDTH)
        title_label.setStyleSheet(
            f"font-size: {FontSize.SUBTITLE.value}px; font-weight: bold;"
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        key_counter = 1
        for button_text in buttons:
            button = QPushButton(f"{key_counter}. {button_text}")
            button.setStyleSheet(f"font-size: {FontSize.NORMAL.value}px;")
            button.setShortcut(QKeySequence(f"{key_counter}"))
            layout.addWidget(button)
            key_counter += 1

        if len(buttons) < 9:
            for _i in range(9 - len(buttons)):
                button = QPushButton(NO_ALBUM_MESSAGE)
                button.setDisabled(True)
                # button = QPushButton(f"{key_counter}. Nope!")
                button.setStyleSheet(f"font-size: {FontSize.NORMAL.value}px;")
                # button.setShortcut(QKeySequence(f'{key_counter}'))
                layout.addWidget(button)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)


from TrackedWindow import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ImgSack")

        main_layout = QHBoxLayout()

        image_label = QLabel(
            "ImgSack\nAlbert Freeman\nhttps://github.com/drivigmenuts/ImgSack"
        )
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setMinimumWidth(768)
        image_label.setMinimumHeight(768)
        if DEBUG:
            logger.debug(r"Adding frame")
            image_label.setFrameShape(QFrame.Shape.Box)
        main_layout.addWidget(image_label)

        self.label_key_layout = QStackedLayout()
        for modifier in MODIFIER_KEYS:
            labels = LabelSetWidget(modifier)
            self.label_key_layout.addWidget(labels)

        utility_keys_layout = QHBoxLayout()
        skip_button_0 = QPushButton("0 - Skip")
        skip_button_0.setStyleSheet(f"font-size: {FontSize.NORMAL.value}px;")
        skip_button_0.setShortcut(QKeySequence("0"))
        trash_button_decimal = QPushButton(". - Trash")
        trash_button_decimal.setStyleSheet(f"font-size: {FontSize.NORMAL.value}px;")
        trash_button_decimal.setShortcut(QKeySequence("."))

        utility_keys_layout.addWidget(skip_button_0)
        utility_keys_layout.addWidget(trash_button_decimal)

        right_column_layout = QVBoxLayout()
        right_column_layout.addLayout(self.label_key_layout)
        right_column_layout.addLayout(utility_keys_layout)
        right_column_layout.addStretch()

        right_column_container = QWidget()
        right_column_container.setMinimumWidth(RIGHT_COLUMN_WIDTH)
        right_column_container.setMaximumWidth(RIGHT_COLUMN_WIDTH)
        right_column_container.setLayout(right_column_layout)

        main_layout.addWidget(right_column_container)

        # main_layout.addLayout(right_column_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def keyPressEvent(self, event: QKeyEvent) -> QKeyEvent:
        super().keyPressEvent(event)
        if event.key() in KEYPRESS_VALUES:
            self.label_key_layout.setCurrentIndex(KEYPRESS_VALUES.index(event.key()))
        return event

    def keyReleaseEvent(self, event: QKeyEvent) -> QKeyEvent:
        super().keyReleaseEvent(event)
        if event.key() in KEYPRESS_VALUES:
            self.label_key_layout.setCurrentIndex(0)
        return event


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
