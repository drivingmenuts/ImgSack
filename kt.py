#!/usr/bin/env python

import logging
import pyglet

from pathlib import Path
from rich import print
from rich.logging import RichHandler

FONT_FILE = Path('./resources/FrederickatheGreat-Regular.ttf').expanduser().as_posix()

logging.basicConfig(level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)

window = pyglet.window.Window(resizable=False, width=640, height=480)
window.set_caption('MouseKeyTest')

logger.info(f'Adding font: {FONT_FILE}')
pyglet.font.add_file(FONT_FILE)

title = pyglet.text.Label('MouseKeyTest',
                          font_name='Fredericka the Great',
                          font_size=64,
                          color=(200, 200, 0, 255),
                          anchor_x='center', anchor_y='bottom',
                          x=window.width // 2, y=(window.height // 2) - 18)
subtitle = pyglet.text.Label('Press any key or ⌘-Q to quit',
                             font_size=14,
                             anchor_x='center', anchor_y='top',
                             x=window.width // 2, y=(window.height // 2))
last_key_label = pyglet.text.Label('',
                                   font_name='American Typewriter Bold',
                                   font_size=18,
                                   color=(200, 200, 255, 255),
                                   anchor_x='center', anchor_y='top',
                                   multiline=True,
                                   width=window.width - 20,
                                   align='center',
                                   x=window.width // 2, y=(window.height // 2) - 64)
origin_label = pyglet.text.Label('⬅︎ Origin (0, 0)',
                                 font_size=14,
                                 anchor_x='left', anchor_y='center',
                                 x=10, y=10,
                                 rotation=-45)
pointer_x_position = pyglet.text.Label('X: 0000 ',
                                       font_size=10,
                                       anchor_x='right', anchor_y='bottom',
                                       x=window.width - 65, y=10)
pointer_y_position = pyglet.text.Label('Y: 0000 ',
                                       font_size=10,
                                       anchor_x='right', anchor_y='bottom',
                                       x=window.width - 15, y=10)


@window.event
def on_draw():
    window.clear()
    title.draw()
    subtitle.draw()
    last_key_label.draw()
    origin_label.draw()
    pointer_x_position.draw()
    pointer_y_position.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):
    pointer_x_position.text = f'X: {x:04}'
    pointer_y_position.text = f'Y: {y:04}'


@window.event
def on_key_press(symbol, modifiers):
    symbol_string = pyglet.window.key.symbol_string(symbol)
    modifiers_string = pyglet.window.key.modifiers_string(modifiers).replace('|', ' | ')
    last_key_label.text = f'{symbol_string} {modifiers_string}'
    if symbol == pyglet.window.key.ESCAPE or symbol == pyglet.window.key.Q:
        print('Quit')
        window.close()
        pyglet.app.exit()


@window.event
def on_key_release(symbol, modifiers):
    last_key_label.text = ''


pyglet.app.run()
