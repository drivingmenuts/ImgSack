#!/usr/bin/env python3

PROGRAM_NAME = "ImageSack"
PROGRAM_VERSION = "0.0.1rNone"
PYTHON_VERSION = "3.9"
VERSION_INFO = f"{PROGRAM_NAME} v{PROGRAM_VERSION} -  Python {PYTHON_VERSION}"

import argparse
import json
import logging
import os
from enum import Enum
from pathlib import Path

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)

logging.info(f"{VERSION_INFO} started")

NO_ALBUM_MESSAGE = "No album defined"
NO_ALBUM_BUTTON_TITLE = "-"
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
MIN_ALBUMS = 9
MAX_ALBUMS = 36  # no mod, shift, alt, ctrl * 9 (on the numeric keypad)


class FontSize(Enum):
    TITLE = 24
    SUBTITLE = 20
    NORMAL = 16
    SMALL = 12
    STATUS_BAR = 12
    TINY = 10


QUICK_MESSAGE_TIMER = 3000
MESSAGE_TIMER = QUICK_MESSAGE_TIMER * 2
# QT swaps key names for modifiers on MacOS. This switches them back.
MODIFIER_KEYS = ["", "Shift", "Ctrl", "Alt"]
KEYPRESS_VALUES = [-1, 16777248, 16777250, 16777251]
DEBUG = True
RIGHT_COLUMN_WIDTH = 384


def is_album(p: Path) -> bool:
    return os.path.isdir(p.expanduser())


def is_not_dotted(p: Path) -> bool:
    return p.name[0] != "."


def move_item(source_file: Path, destination_folder: Path) -> None:
    logger.info(f"Moving {source_file} to {destination_folder}")
    source_file.rename(destination_folder / source_file.name)


class StatusWidget(QWidget):
    def __init__(self, working_directory: Path = "Testing/", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()

        if working_directory is not None:
            dir_label = QLabel(f"{working_directory}")
            dir_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
            layout.addWidget(dir_label)

        ver_label = QLabel(f"<b>{PROGRAM_NAME}</b> v{PROGRAM_VERSION}")
        layout.addWidget(ver_label)

        self.setLayout(layout)


class LabelSetWidget(QFrame):
    def __init__(self, title: str, buttons=None, parent=None):
        super().__init__(parent)
        if buttons is None:
            logger.critical("Buttons cannot be None in LabelSetWidget.__init__")
            exit(1)
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
                button = QPushButton()
                button.setDisabled(True)
                # button = QPushButton(f"{key_counter}. Nope!")
                button.setStyleSheet(f"font-size: {FontSize.NORMAL.value}px;")
                # button.setShortcut(QKeySequence(f'{key_counter}'))
                layout.addWidget(button)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(
        self,
        source_dir: Path,
        album_dir: Path,
        album_lst: list,
        parent=None,
    ):
        logger.debug(f"MainWindow got source_dir: {source_dir}")
        logger.debug(f"MainWindow got album_dir: {album_dir}")
        logger.debug(f"MainWindow got album_lst: {album_lst}")

        super().__init__(parent=parent)

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
        # TODO: do this as an iterable?
        labels_none = LabelSetWidget("", album_lst[0:9])
        self.label_key_layout.addWidget(labels_none)
        labels_shift = LabelSetWidget("Shift", album_lst[9:18])
        self.label_key_layout.addWidget(labels_shift)
        labels_ctrl = LabelSetWidget("Ctrl", album_lst[18:27])
        self.label_key_layout.addWidget(labels_ctrl)
        labels_alt = LabelSetWidget("Alt", album_lst[27:36])
        self.label_key_layout.addWidget(labels_alt)

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

        self.statusBar().addPermanentWidget(StatusWidget())
        self.statusBar().showMessage("Ready", QUICK_MESSAGE_TIMER)
        self.show()

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"{VERSION_INFO}")
    parser.add_argument(
        "-s", "--source", help="source directory for images", default="."
    )
    parser.add_argument(
        "-a", "--albums", help="directory for album folders", default=None
    )
    parser.add_argument("-c", "--config", help="configuration file", default=None)
    parser.add_argument(
        "-e",
        "--extensions",
        help="list of image extensions",
        default=DEFAULT_EXTENSIONS,
    )
    args = parser.parse_args()

    if args.config is not None:
        config_file = Path(args.config).expanduser().resolve()
        if not config_file.exists():
            logging.critical(f"Configuration file {args.config} does not exist")
            exit(1)
        config = json.loads(config_file.read_text())
        source_directory = Path(config["source_directory"]).expanduser().resolve()
        album_directory = Path(config["output_directory"]).expanduser().resolve()
        albums = config["albums"]
        logging.critical("Config - Not implemented yet")
        exit(1)
    else:
        source_directory = Path(args.source).expanduser().resolve()
        logger.debug(f"Source Directory: {source_directory}")
        if not source_directory.exists():
            logging.critical(f"Source directory {args.source} does not exist")
            exit(1)

        if args.albums is None:
            album_directory = source_directory
        else:
            album_directory = Path(args.albums).expanduser().resolve()
            logger.debug(f"Album Directory: {album_directory}")
            if not album_directory.exists():
                logging.critical(f"Album directory {args.albums} does not exist")
                exit(1)

    album_list = []
    for d in album_directory.iterdir():
        logger.debug(f"{d} is_album: {is_album(d)} is_not_dotted: {is_not_dotted(d)}")
        if is_album(d) and is_not_dotted(d):
            album_list.append(d.name)

    album_list.sort()

    if len(album_list) < 1:
        logging.critical(f"Album directory {album_directory} has no albums")
        exit(1)
    if len(album_list) < MIN_ALBUMS:
        logging.info(
            f"Album directory {album_directory} has {len(album_list)} albums - padding to {MIN_ALBUMS}"
        )
        album_list = album_list + [NO_ALBUM_BUTTON_TITLE] * (
            MAX_ALBUMS - len(album_list)
        )
    if len(album_list) > MAX_ALBUMS:
        logging.warning(
            f"Album directory {album_directory} has too many albums - truncating to {MAX_ALBUMS}"
        )
        album_list = album_list[:MAX_ALBUMS]

    item_list = [
        Path(f).expanduser()
        for f in source_directory.iterdir()
        if Path(f).expanduser().suffix in DEFAULT_EXTENSIONS
    ]
    logger.info(f"{len(item_list)} items found in {source_directory}")

    app = QApplication([])

    window = MainWindow(source_directory, album_directory, album_list)
    window.show()

    app.exec()
