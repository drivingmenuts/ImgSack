#!/usr/bin/env python3

PROGRAM_NAME = 'ImageSack'
PROGRAM_VERSION = '0.0.1rNone'
PYTHON_VERSION = '3.9'
VERSION_INFO = f'{PROGRAM_NAME} v{PROGRAM_VERSION} - {PYTHON_VERSION}'

import argparse
import logging
import json
import os

from pathlib import Path
from rich.logging import RichHandler

logging.basicConfig(level='NOTSET', format='%(message)s', datefmt='[%X]', handlers=[RichHandler(rich_tracebacks=True)])
logger = logging.getLogger(__name__)

logging.info(f'{VERSION_INFO} started')

DEFAULT_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.webp', '.svg']
MAX_ALBUMS = 36  # no mod, shift, alt, ctrl * 9 (on the numeric keypad)


def is_album(p: Path) -> bool:
    return os.path.isdir(p.expanduser())


def is_not_dotted(p: Path) -> bool:
    return str(p.expanduser()).split('/')[:-1][0] != '.'


def move_item(source_file: Path, destination_folder: Path) -> None:
    logger.info(f'Moving {source_file} to {destination_folder}')
    source_file.rename(destination_folder / source_file.name)


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
    logging.warning(f'Album directory {album_directory} has too many albums - truncating to {MAX_ALBUMS}')
    album_list = album_list[:MAX_ALBUMS]

item_list = [Path(f).expanduser() for f in source_directory.iterdir() if
             Path(f).expanduser().suffix in DEFAULT_EXTENSIONS]
logger.info(f'{len(item_list)} items found in {source_directory}')