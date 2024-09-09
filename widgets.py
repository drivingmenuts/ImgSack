#!/usr/bin/env python3

import sys
from pathlib import Path

from PySide6.QtWidgets import *

from d4mnLogger import logger


class AboutBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("About")


class ActionButton(QPushButton):
    _action = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "action" in kwargs:
            self._action = kwargs["action"]
        else:
            self.setEnabled(False)

    def getAction(self):
        return self._action

    def setAction(self, func):
        self._action = func
        self.setEnabled(True)
        return self

    def keyReleaseEvent(self, e):
        return self._action(e)

    def mouseReleaseEvent(self, e):
        return self.keyPressEvent(e)


class Image(QLabel):
    _max_width = 512
    _max_height = 512
    _file = None
    _file_width = 0
    _file_height = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        if "max_width" in kwargs:
            self._max_width = kwargs["max_width"]
        if "max_height" in kwargs:
            self._max_height = kwargs["max_height"]


class StatusBar(QStatusBar):
    _areas = dict()

    def __init__(self, area_list: list, font_size: int = 12, skip_name: bool = False):
        super().__init__()
        logger.debug(f"StatusBar got area_list: {area_list}")

        layout = QHBoxLayout()
        for area in area_list:
            logger.debug(f"Adding: {area}")
            self._areas[area] = QLabel(f"Area; {area}")
            self._areas[area].setStyleSheet(f"font-size: {font_size}px;")
            layout.addWidget(self._areas[area])

        right_container = QWidget()
        right_container.setLayout(layout)
        self.addPermanentWidget(right_container)

        if skip_name is not True:
            program_name = QLabel(f"{Path(sys.argv[0]).name}")
            program_name.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
            self.addPermanentWidget(program_name)

    def setArea(self, area: str, message: str, timeout: int = 0):
        if area in self._areas.keys():
            self._areas[area].setText(message)


if __name__ == "__main__":
    from PySide6.QtCore import QSize
    from PySide6.QtWidgets import QApplication, QMainWindow

    app = QApplication([])

    window = QMainWindow()
    window.setWindowTitle(f"{sys.argv[0]}")
    window.resize(QSize(800, 600))

    _status = StatusBar(["Area 51", "Area 52"], font_size=10)
    window.setStatusBar(_status)
    if window.statusBar() is not None:
        logger.debug(window.statusBar())

    window.show()

    _status.showMessage("Ready", 5000)
    _status.setArea("Area 51", "I'm ready!")

    action_button = ActionButton()
    action_button.setText("Action Button")
    action_button.setAction(lambda e: logger.info("Action Button was pressed!"))

    window.setCentralWidget(action_button)

    about = AboutBox()
    about.setText("ImgSack")
    about.setInformativeText("ImgSack is a tool for managing your image collection.")
    about.show()

    app.exec()
    app.quit()
