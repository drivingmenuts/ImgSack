#!/usr/bin/env python3
PROGRAM_NAME = 'ImageSack'
PROGRAM_VERSION = '0.0.1rNone'
VERSION_INFO = f'{PROGRAM_NAME} v{PROGRAM_VERSION}'

import logging
import os
import pyglet

from enum import Enum
from pathlib import Path
from rich.logging import RichHandler

logging.basicConfig(level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)

logging.info(f'{VERSION_INFO} started')

_resolution = (1280, 1024)
MINIMUM_RESOLUTION = (640, 480)
IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.webp', '.heic', '.heif', '.avif']


class KeyingMode(Enum):
    # The value is the maximum number of albums supported by the mode
    K9 = 27
    K10 = 999


key_mode = KeyingMode.K9


class ImageList:
    def __init__(self, source_directory: Path, filter_func=None):
        self._source_directory = source_directory
        self._filter_func = filter_func

    def __iter__(self):
        return self

    def __next__(self):
        next_file = next(os.scandir(self._source_directory))

    def __len__(self):
        return len(os.listdir(self._source_directory)).filter(self._filter_func)


def get_album_list(source_dir: Path) -> list:
    directories = []
    for path in source_dir.iterdir():
        if path.is_dir():
            directories.append(path.name)
    directories.sort()

    logging.debug(f'Album list: {directories}')
    return directories


def get_image_list(source_dir: Path) -> list:
    images = []
    for filename in source_dir.iterdir():
        if filename.is_file() and filename.suffix in IMAGE_FORMATS:
            images.append(filename.name)
    images.sort()

    logging.debug(f'{len(images)} images found in {source_dir}')
    return images


def app(source_dir: Path, albums_dir: Path, album_list: list):
    window = pyglet.window.Window(resizable=True, width=_resolution[0], height=_resolution[1])
    window.set_minimum_size(MINIMUM_RESOLUTION[0], MINIMUM_RESOLUTION[1])

    images = get_image_list(Path(source_dir))

    @window.event
    def on_resize(width: int, height: int) -> None:
        global _resolution

        _resolution = (width, height)
        logging.info(f'Window size set to {_resolution[0]}x{_resolution[1]}')

    pyglet.app.run()


if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser(description=f'{VERSION_INFO}')
    parser.add_argument('-s', '--source', help='source directory for images',
                        default='.')
    parser.add_argument('-a', '--albums', help='directory for album folders',
                        default=None)
    parser.add_argument('-c', '--config', help='configuration file',
                        default=None)
    parser.add_argument('-k', '--keymode', help='keying mode (see help)',
                        choices=[k.name.lower() for k in KeyingMode],
                        default=KeyingMode.K9.name.lower())

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

        albums = get_album_list(album_directory)

        if args.keymode is not None:
            logging.warning('Keymode - Not implemented yet')

    app(source_directory, album_directory, albums)
    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
