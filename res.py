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

RES_HORIZONTAL = 1280
RES_VERTICAL = 720
BOX_WIDTH_HORIZONTAL = 16
BOX_HEIGHT_VERTICAL = 16
MAX_LINES = RES_VERTICAL // BOX_HEIGHT_VERTICAL
MAX_COLUMNS = RES_HORIZONTAL // BOX_WIDTH_HORIZONTAL
GRID_COLOR = (255, 255, 255, 48)
LINE_WIDTH = 1.5


class FontSizes(Enum):
    TITLE = 64
    SUBTITLE = 32
    NORMAL = 16
    SMALL = 10
    TINY = 8


Point = namedtuple('Point', ['x', 'y'])

line_column = (
    lambda line, col: Point((col - 1) * BOX_WIDTH_HORIZONTAL, RES_VERTICAL - ((line - 1) * BOX_HEIGHT_VERTICAL)))


def get_line_column(line: int, column: int) -> Point:
    x = (column - 1) * BOX_WIDTH_HORIZONTAL
    y = RES_VERTICAL - ((line - 1) * BOX_HEIGHT_VERTICAL)
    return Point(x, y)


logger.debug(f'Max Lines: {MAX_LINES} Max Columns: {MAX_COLUMNS}')


def mk_grid(horizontal_resolution: int, box_width: int,
            vertical_resolution: int, box_height: int,
            grid_color: (int, int, int, int),
            line_width: float) -> pyglet.graphics.Batch:
    batch = pyglet.graphics.Batch()
    h_lines = []
    logger.info(f'horizontal grid lines')
    for h_line_y in range(1, vertical_resolution, box_height):
        p1 = Point(0, h_line_y)
        p2 = Point(horizontal_resolution, h_line_y)
        logger.info(f'x1:{p1.x:04.2f} y1:{p1.y:04.2f} x2:{p2.x:04.2f} y2:{p2.y:04.2f}')
        h_lines.append(pyglet.shapes.Line(x=p1.x,
                                          y=p1.y,
                                          x2=p2.x,
                                          y2=p2.y,
                                          width=line_width,
                                          color=grid_color,
                                          batch=batch,
                                          blend_src=pyglet.gl.GL_SRC_ALPHA,
                                          blend_dest=pyglet.gl.GL_ONE_MINUS_DST_ALPHA))

    v_lines = []
    logger.info(f'vertical grid lines')
    for y_line_x in range(1, horizontal_resolution, box_width):
        p1 = Point(y_line_x, 0)
        p2 = Point(y_line_x, vertical_resolution)
        logger.info(f'x1:{p1.x:04.2f} y1:{p1.y:04.2f} x2:{p2.x:04.2f} y2:{p2.y:04.2f}')
        v_lines.append(pyglet.shapes.Line(x=p1.x,
                                          y=p1.y,
                                          x2=p2.x,
                                          y2=p2.y,
                                          width=line_width,
                                          color=grid_color,
                                          batch=batch,
                                          blend_src=pyglet.gl.GL_SRC_ALPHA,
                                          blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA))

    pprint(batch.__dict__)
    return batch


grid_batch = mk_grid(RES_HORIZONTAL, BOX_WIDTH_HORIZONTAL, RES_VERTICAL, BOX_HEIGHT_VERTICAL, GRID_COLOR, LINE_WIDTH)
p_title = line_column(2, 2)
logger.info(f'x1:{p_title.x:04.2f} y1:{p_title.y:04.2f}')
title_label = pyglet.text.Label('Resolution & Grid Test',
                                font_size=FontSizes.TINY.value,
                                bold=True,
                                color=(200, 200, 255, 255),
                                anchor_x='left', anchor_y='top',
                                x=p_title.x, y=p_title.y)

main_window = pyglet.window.Window(resizable=False,
                                   width=1280,
                                   height=720,
                                   caption='Resolution & Grid Test')


@main_window.event
def on_draw():
    main_window.clear()
    grid_batch.draw()
    title_label.draw()


@main_window.event
def on_redraw():
    on_draw()


pyglet.app.run()
