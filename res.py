#!/usr/bin/env python3
import logging

from collections import namedtuple
from enum import Enum
from rich.pretty import pprint
from rich.logging import RichHandler

logging.basicConfig(level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)

logger.info('res starting')
import pyglet

Point = namedtuple('Point', ['x', 'y'])
Color = namedtuple('Color', ['r', 'g', 'b'])

RES_HORIZONTAL = 1280
RES_VERTICAL = 720
BOX_WIDTH = 16
BOX_HEIGHT = 16
MAX_LINES = RES_VERTICAL // BOX_HEIGHT
MAX_COLUMNS = RES_HORIZONTAL // BOX_WIDTH
GRID_COLOR = (255, 255, 255, 48)
LINE_WIDTH = 1.5
TITLE_FONT = 'resources/api.ttf'


def shade(self, color: str, alpha: float) -> Color:
    _colors = {
        'black': Color(0, 0, 0),
        'white': Color(255, 255, 255),
        'red': Color(255, 0, 0),
        'green': Color(0, 255, 0),
        'blue': Color(0, 0, 255),
        'yellow': Color(255, 255, 0),
        'cyan': Color(0, 255, 255),
        'magenta': Color(255, 0, 255),
    }
    amount = int(255 * alpha)
    r, g, b = _colors[color.lower()]
    return Color(r, g, b, amount)


class FontSizes(Enum):
    TITLE = BOX_HEIGHT * 2
    SUBTITLE = 32
    NORMAL = 16
    SMALL = 10
    TINY = 8


line_column = (lambda line, col: Point((col - 1) * BOX_WIDTH, RES_VERTICAL - ((line - 1) * BOX_HEIGHT)))


def get_line_column(line: int, column: int) -> Point:
    x = (column - 1) * BOX_WIDTH
    y = RES_VERTICAL - ((line - 1) * BOX_HEIGHT)
    return Point(x, y)


logger.debug(f'Max Lines: {MAX_LINES} Max Columns: {MAX_COLUMNS}')

grid_batch = pyglet.graphics.Batch()
horizontal_lines = pyglet.graphics.Group(order=0)
vertical_lines = pyglet.graphics.Group(order=1)
h_lines = []
logger.info(f'horizontal grid lines')
for h_line_y in range(1, RES_VERTICAL, BOX_HEIGHT):
    p1 = Point(0, h_line_y)
    p2 = Point(RES_HORIZONTAL, h_line_y)
    logger.info(f'x1:{p1.x:04.2f} y1:{p1.y:04.2f} x2:{p2.x:04.2f} y2:{p2.y:04.2f}')
    h_lines.append(pyglet.shapes.Line(x=p1.x,
                                      y=p1.y,
                                      x2=p2.x,
                                      y2=p2.y,
                                      width=LINE_WIDTH,
                                      color=GRID_COLOR,
                                      batch=grid_batch,
                                      group=horizontal_lines,
                                      blend_src=pyglet.gl.GL_SRC_ALPHA,
                                      blend_dest=pyglet.gl.GL_ONE_MINUS_DST_ALPHA))

v_lines = []
logger.info(f'vertical grid lines')
for y_line_x in range(1, RES_HORIZONTAL, BOX_WIDTH):
    p1 = Point(y_line_x, 0)
    p2 = Point(y_line_x, RES_VERTICAL)
    logger.info(f'x1:{p1.x:04.2f} y1:{p1.y:04.2f} x2:{p2.x:04.2f} y2:{p2.y:04.2f}')
    v_lines.append(pyglet.shapes.Line(x=p1.x,
                                      y=p1.y,
                                      x2=p2.x,
                                      y2=p2.y,
                                      width=LINE_WIDTH,
                                      color=GRID_COLOR,
                                      batch=grid_batch,
                                      group=vertical_lines,
                                      blend_src=pyglet.gl.GL_SRC_ALPHA,
                                      blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA))

p_title = line_column(2, 2)
pyglet.font.add_file(TITLE_FONT)
title_font = pyglet.font.load('Armor Piercing', 64)
logger.info(f'x1:{p_title.x:04.2f} y1:{p_title.y:04.2f}')

title_label = pyglet.text.Label('IMGSACK',
                                font_name='Armor Piercing',
                                font_size=FontSizes.TITLE.value,
                                bold=True,
                                color=(200, 200, 255, 255),
                                anchor_x='left', anchor_y='top',
                                x=p_title.x, y=p_title.y)

stage_point = get_line_column(2,2)
logger.info(f'x1:{stage_point.x:04.2f} y1:{stage_point.y:04.2f}')
shape_stage = pyglet.shapes.Box(stage_point.x, stage_point.y, width=640,height=640, color=(255, 255, 255, 160), anchor_x='left', anchor_y='top')

main_window = pyglet.window.Window(resizable=False,
                                   width=1280,
                                   height=720,
                                   caption='Resolution & Grid Test')


@main_window.event
def on_draw():
    main_window.clear()
    grid_batch.draw()
    title_label.draw()
    shape_stage.draw()


@main_window.event
def on_redraw():
    on_draw()


pyglet.app.run()
