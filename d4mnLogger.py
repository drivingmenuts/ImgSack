#!/usr/bin/env python3

import logging

from rich.logging import RichHandler

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)

logging.info("d4mnLogger started")

_all__ = ["logger"]
