#!/usr/bin/env python

import logging
import pyglet

from rich.logging import RichHandler

logging.basicConfig(level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)

window = pyglet.window.Window(resizable=False, width=640, height=480)
window.set_caption('MouseKeyTest')
title = pyglet.text.Label('MouseKeyTest',
                          font_name='Fredericka the Great',
                          font_size=64,
                          anchor_x='center', anchor_y='bottom',
                          x=window.width // 2, y=(window.height // 2)-18)
subtitle = pyglet.text.Label('Press any key or ⌘-Q to quit',
                             font_size=14,
                             anchor_x='center', anchor_y='top',
                             x=window.width // 2, y=(window.height // 2))
origin_label = pyglet.text.Label('🡄 Origin (0, 0)',
                                 font_size=14,
                                 anchor_x='left', anchor_y='center',
                                 x=10, y=10,
                                 rotation=-45)
pointer_x_label = pyglet.text.Label('X: 0000 ',
                                    font_size=10,
                                    anchor_x='right', anchor_y='bottom',
                                    x=window.width - 60, y=10)
pointer_y_label = pyglet.text.Label('Y: 0000 ',
                                    font_size=10,
                                    anchor_x='right', anchor_y='bottom',
                                    x=window.width - 10, y=10)


@window.event
def on_key_press(symbol, modifiers):
    print(symbol, modifiers)


@window.event
def on_draw():
    window.clear()
    title.draw()
    subtitle.draw()
    origin_label.draw()
    pointer_x_label.draw()
    pointer_y_label.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):
    pointer_x_label.text = f'X: {x:04}'
    pointer_y_label.text = f'Y: {y:04}'


pyglet.app.run()
