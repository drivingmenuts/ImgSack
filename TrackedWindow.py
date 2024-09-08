from __future__ import annotations

from typing import Union

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QMainWindow
from rich import print

print('EventTracker started')

EventTitle = Union[str, QEvent]


def print_event(event_title: EventTitle = None, vars_dict: dict = dict):
    """
    Print an event to the console.

    If `event_title` is `None`, then the type of the `event` is used as the title.
    Otherwise, `event_title` is used as the title.

    `vars_dict` is a dictionary of variables to be printed below the title.
    Each item in the dictionary is printed with its key and value separated by a colon.
    """
    if event_title is None:
        if isinstance(event, QEvent):
            event_title = type(event).__name__
        else:
            event_title = event.text()

    print(f'{event_title}\n' + '\n'.join(f'\t{k}: {v}' for k, v in vars_dict.items()) + '\n')


def _print_key_event(event: QKeyEvent):
    """
    Print a QKeyEvent to the console.

    The event is printed with the title `:key: ({Qt.Key(event.key()).name})`.
    The printed dictionary contains the following information:
        key: The key that was pressed.
        text: The text of the key that was pressed.
        modifiers: The Qt modifiers of the key that was pressed.
        nativeModifiers: The native modifiers of the key that was pressed.
        autoRepeat: Whether the key is being auto-repeated.
    """
    print_event(f':key: ({Qt.Key(event.key()).name})', {
        'key': event.key(),
        'text': event.text(),
        'modifiers': event.modifiers(),
        'nativeModifiers': event.nativeModifiers(),
        'autoRepeat': event.isAutoRepeat(),
    })


def _print_mouse_event(event: QMouseEvent):
    """
    Print a QMouseEvent to the console.

    The event is printed with the title `:mouse: ({event.button()})`.
    The printed dictionary contains the following information:
        globalPos: The global position of the mouse cursor.
        localPos: The position of the mouse cursor relative to the widget.
        screenPos: The position of the mouse cursor relative to the screen.
        windowPos: The position of the mouse cursor relative to the window.
    """
    print_event(f':mouse: ({event.button()})', {
        'globalPos': event.globalPos(),
        'localPos': event.localPos(),
        'screenPos': event.screenPos(),
        'windowPos': event.windowPos(),
    })


class TrackedWindow(QMainWindow):
    def keyPressEvent(self, event: QKeyEvent) -> QKeyEvent:
        """
        Print a QKeyEvent to the console and pass it through to the parent method.

        The event is printed with the title `:key: ({Qt.Key(event.key()).name})`.
        The printed dictionary contains the following information:
            key: The key that was pressed.
            text: The text of the key that was pressed.
            modifiers: The Qt modifiers of the key that was pressed.
            nativeModifiers: The native modifiers of the key that was pressed.
            autoRepeat: Whether the key is being auto-repeated.

        The event is then passed through to the parent method.
        """
        _print_key_event(event)
        return event

    def mouseReleaseEvent(self, event: QMouseEvent) -> QMouseEvent:
        """
        Print a QMouseEvent to the console and pass it through to the parent method.

        The event is printed with the title `:mouse: ({event.button()})`.
        The printed dictionary contains the following information:
            globalPos: The global position of the mouse cursor.
            localPos: The position of the mouse cursor relative to the widget.
            screenPos: The position of the mouse cursor relative to the screen.
            windowPos: The position of the mouse cursor relative to the window.

        The event is then passed through to the parent method.
        """
        _print_mouse_event(event)
        return event


__all__ = ['TrackedWindow', 'print_event']
