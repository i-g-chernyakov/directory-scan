# -*- coding: utf-8 -*-

"""
Patch for aiologger.

aiologger (https://github.com/B2W-BIT/aiologger) implements 'async/await' syntax
for logging. But there is a problem with aiologger working in Windows.

The stdout and stderr streams in aiologger are connected as pipes. But in
Windows it doesn't work.

The modified stream handler DSAsyncStreamHandler is used in this patch.

"""

from typing import Callable, Optional

from directory_scan.dsaiologger.json import DSJsonLogger
from directory_scan.dsaiologger.logger import DSLogger


__all__ = ['DSLogger', 'DSJsonLogger', 'get_logger', 'remove_logger',
           'set_logger']

_logger: Optional[DSLogger] = None


def get_logger() -> Callable[[], Optional[DSLogger]]:
    """Return logger.

    If is no logger create it first
    """

    def factory():
        global _logger

        if _logger is None:
            _logger = DSJsonLogger.with_default_handlers()

        return _logger

    return factory


def set_logger(logger: DSLogger) -> None:
    """Set global logger. If logger exists"""
    global _logger
    _logger = logger


def remove_logger() -> None:
    """Remove logger"""
    global _logger
    _logger = None
