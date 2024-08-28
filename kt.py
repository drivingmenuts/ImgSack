#!/usr/bin/env python

import logging
import pyglet

from rich.logging import RichHandler

logging.basicConfig(level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)

window = pyglet.window.Window(resizable=False, width=640, height=480)
print('Press any key until you are done. Then press CMD-Q to quit.')


@window.event
def on_key_press(symbol, modifiers):
    print(symbol, modifiers)


pyglet.app.run()
