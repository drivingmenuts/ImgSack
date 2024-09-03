#!/usr/bin/env python3

PROGRAM_NAME = 'ImageSack'
PROGRAM_VERSION = '0.0.1rNone'
PYTHON_VERSION = '3.9'
VERSION_INFO = f'{PROGRAM_NAME} v{PROGRAM_VERSION} - {PYTHON_VERSION}'

import argparse
import logging
import json
import os
import pyglet

from collections import namedtuple
from enum import Enum
from pathlib import Path
from pyglet.font import ttf
from rich.logging import RichHandler
from rich.pretty import pprint

logging.basicConfig(level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)

logging.info(f'{VERSION_INFO} started')

Point = namedtuple('Point', ['x', 'y'])
FrameSize = namedtuple('FrameSize', ['width', 'height'])

screen = pyglet.canvas.get_display().get_default_screen()
# window_size = FrameSize(width=(screen.width // 3) * 2, height=screen.height)
window_size = FrameSize(1280, 720)
logging.debug(f'Window Size: {window_size}')

DEFAULT_INNER_MARGIN = 8
MINIMUM_RESOLUTION = FrameSize(920, 640)
DEFAULT_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.webp', '.svg']
MAX_ALBUMS = 36  # no mod, shift, alt, ctrl * 9 (on the numeric keypad)
TITLE_FONT_FILE = (Path('./resources/luckiest-guy/LuckiestGuy.ttf')
                   #.expanduser()
                   #.as_posix())


class FontSizes(Enum):
    TITLE = 64
    SUBTITLE = 32
    NORMAL = 24
    SMALL = 18
    TINY = 12


class Colors(Enum):
    TITLE = (200, 200, 0, 255)
    SUBTITLE = (200, 200, 200, 255)
    NORMAL = (200, 200, 200, 255)
    SMALL = (200, 200, 200, 255)
    TINY = (200, 200, 200, 255)
    FRAME = (255, 255, 255, 64)


class Stage:
    def __init__(self, frame_size: FrameSize, max_horizontal: int, max_vertical: int,
                 margin: int = DEFAULT_INNER_MARGIN) -> None:
        self._max_horizontal = max_horizontal
        self._max_vertical = max_vertical
        self._frame_size = int(frame_size.width * (self._max_horizontal / 100))
        self._window_height = int(frame_size.height * (self._max_vertical / 100))
        self._sizing = Sizing(self._window_width, self._window_height, margin)


class Sizing:
    def __init__(self, width: int, height: int, margin: int = DEFAULT_INNER_MARGIN) -> None:
        if width < MINIMUM_RESOLUTION.width:
            width = MINIMUM_RESOLUTION.width
            logging.debug(f'Minimum Window Width: {width}')

        if height < MINIMUM_RESOLUTION.height:
            height = MINIMUM_RESOLUTION.height
            logging.debug(f'Minimum Window Height: {height}')

        if margin < 0:
            margin = 0

        self._width = width
        self._height = height
        self._margin = margin
        self._anchors = {
            'left': {
                'top': Point(0 + self._margin, self._height - self._margin),
                'center': Point(0 + self._margin, self._height // 2),
                'bottom': Point(0 + self._margin, 0 + self._margin)
            },
            'right': {
                'top': Point(self._width - self._margin, self._height - self._margin),
                'center': Point(self._width - self._margin, self._height // 2),
                'bottom': Point(self._width - self._margin, 0 + self._margin)
            },
            'top': {
                'left': Point(0 + self._margin, self._height - self._margin),
                'center': Point(self._width // 2, self._height - self._margin),
                'right': Point(self._width - self._margin, self._height - self._margin)
            },
            'bottom': {
                'left': Point(0 + self._margin, 0 + self._margin),
                'center': Point(self._width // 2, 0 + self._margin),
                'right': Point(self._width - self._margin, 0 + self._margin)
            },
            'center': {
                'top': Point(self._width // 2, self._height - self._margin),
                'center': Point(self._width // 2, self._height // 2),
                'bottom': Point(self._width // 2, 0 + self._margin),
                'left': Point(0 + self._margin, self._height // 2),
                'right': Point(self._width - self._margin, self._height // 2)
            }
        }

    def get_position(self, anchor_x: pyglet.customtypes.HorizontalAlign,
                     anchor_y: pyglet.customtypes.ContentVAlign) -> tuple:
        return Point(self._anchors[anchor_x][anchor_y].x, self._anchors[anchor_x][anchor_y].y)

    def dump(self) -> None:
        if logger.level <= logging.DEBUG:
            pprint('=' * 40)
            pprint(f'Window Size: {self._width}x{self._height}')
            pprint(f'Margin: {self._margin}')
            pprint(f'Anchors: {self._anchors}')
            pprint('=' * 40)


anchors = Sizing(window_size.width, window_size.height)
anchors.dump()


def is_album(p: Path) -> bool:
    return os.path.isdir(p.expanduser())


def is_not_dotted(p: Path) -> bool:
    return str(p.expanduser()).split('/')[:-1][0] != '.'


def move_item(source_file: Path, destination_folder: Path) -> None:
    logger.info(f'Moving {source_file} to {destination_folder}')


def get_font(font_file: Path) -> str:
    pyglet.font.add_file(TITLE_FONT_FILE)
    return ttf.TruetypeInfo(TITLE_FONT_FILE).get_name('name')


# ## Main #############################

parser = argparse.ArgumentParser(description=f'{VERSION_INFO}')
parser.add_argument('-s', '--source', help='source directory for images',
                    default='.')
parser.add_argument('-a', '--albums', help='directory for album folders',
                    default=None)
parser.add_argument('-c', '--config', help='configuration file',
                    default=None)
parser.add_argument('-e', '--extensions', help='list of image extensions',
                    default=DEFAULT_EXTENSIONS)
args = parser.parse_args()

if args.config is not None:
    config_file = Path(args.config).expanduser().resolve()
    if not config_file.exists():
        logging.critical(f'Configuration file {args.config} does not exist')
        exit(1)
    config = json.loads(config_file.read_text())
    source_directory = Path(config['source_directory']).expanduser().resolve()
    album_directory = Path(config['output_directory']).expanduser().resolve()
    albums = config['albums']
    logging.critical('Config - Not implemented yet')
    exit(1)
else:
    source_directory = Path(args.source).expanduser().resolve()
    if not source_directory.exists():
        logging.critical(f'Source directory {args.source} does not exist')
        exit(1)

    if args.albums is None:
        album_directory = source_directory
    else:
        album_directory = Path(args.albums).expanduser().resolve()
        if not album_directory.exists():
            logging.critical(f'Album directory {args.albums} does not exist')
            exit(1)

album_list = [Path(d).expanduser() for d in album_directory.iterdir() if is_album(d) and is_not_dotted(d)]
if len(album_list) < 1:
    logging.critical(f'Album directory {album_directory} has no albums')
    exit(1)
if len(album_list) < MAX_ALBUMS:
    logging.info(f'Album directory {album_directory} has {len(album_list)} albums - padding to {MAX_ALBUMS}')
    album_list = album_list + ['-'] * (MAX_ALBUMS - len(album_list))
if len(album_list) > MAX_ALBUMS:
    logging.critical(f'Album directory {album_directory} has too many albums - truncating to {MAX_ALBUMS}')
    album_list = album_list[:MAX_ALBUMS]

item_list = [Path(f).expanduser() for f in source_directory.iterdir() if
             Path(f).expanduser().suffix in DEFAULT_EXTENSIONS]
logger.info(f'{len(item_list)} items found in {source_directory}')

title_font = get_font(TITLE_FONT_FILE)
main_window = pyglet.window.Window(resizable=False, width=window_size.width, height=window_size.height,
                                   caption=VERSION_INFO)
title = pyglet.text.Label(PROGRAM_NAME,
                          font_name=title_font,
                          font_size=FontSizes.TITLE.value,
                          color=Colors.TITLE.value,
                          x=anchors.get_position('left', 'top').x,
                          y=anchors.get_position('left', 'top').y,
                          anchor_x='left', anchor_y='top')
copyright = pyglet.text.Label('Copyright 2024, Albert Freeman, MIT License',
                              font_size=FontSizes.TINY.value,
                              color=Colors.TINY.value,
                              x=anchors.get_position('left', 'bottom').x,
                              y=anchors.get_position('left', 'bottom').y,
                              anchor_x='left', anchor_y='bottom')


@main_window.event
def on_draw() -> None:
    main_window.clear()
    title.draw()
    copyright.draw()


@main_window.event
def on_resize(width: int, height: int) -> None:
    # if we're too small, just resize to the minimum
    if width < MINIMUM_RESOLUTION.width:
        main_window.width = MINIMUM_RESOLUTION.width
        width = MINIMUM_RESOLUTION.width
        logging.debug(f'Minimum Window Width: {main_window.width}')

    if height < MINIMUM_RESOLUTION.height:
        main_window.height = MINIMUM_RESOLUTION.height
        height = MINIMUM_RESOLUTION.height
        logging.debug(f'MinimumWindow Height: {main_window.height}')

    updated_window_size = FrameSize(width, height)
    logger.debug(f'Window Size: {updated_window_size}')

    updated_anchors = Sizing(updated_window_size.width, updated_window_size.height)
    logger.debug(f'Window Anchors: {updated_anchors}')

    # there's probably a better way of handling this
    title.x, title.y = updated_anchors.get_position('left', 'top')
    copyright.x, copyright.y = updated_anchors.get_position('left', 'bottom')


pyglet.app.run()
