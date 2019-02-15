# -*- coding: utf-8 -*-

"""
Patch for aiologger.logger.Logger

aiologger (https://github.com/B2W-BIT/aiologger) implements 'async/await' syntax
for logging. But there is a problem with aiologger working in Windows.

The stdout and stderr streams in aiologger are connected as pipes. But in
Windows it doesn't work.

In the DSLogger we use the modified stream handler DSAsyncStreamHandler.

And there is a method for changing of logging level yet.

"""

import logging
import sys
from asyncio import AbstractEventLoop
from typing import Optional, Union

from aiologger.filters import StdoutFilter
from aiologger.logger import Logger

from directory_scan.dsaiologger.handlers import DSAsyncStreamHandler

LoggingLevel = Union[int, str]
OptionalLoggingFormatter = Optional[logging.Formatter]
OptionalAbstractEventLoop = Optional[AbstractEventLoop]


class DSLogger(Logger):
    """Patch for class aiologger.logger.Logger.

    There is patched method `DSLogger.with_default_handlers` (use modified class
    DSAsyncStreamHandler). And method `DSLogger.set_level` is added.
    """

    def __init__(
        self,
        *,
        name: str = "dslogger",
        level: LoggingLevel = logging.NOTSET,
        loop: OptionalAbstractEventLoop = None
    ) -> None:
        """Init logger."""
        super().__init__(name=name, level=level, loop=loop)
        self._stdout_handler: DSAsyncStreamHandler = None
        self._stderr_handler: DSAsyncStreamHandler = None

    @classmethod
    def with_default_handlers(
        cls,
        *,
        name: str = "dslogger",
        level: LoggingLevel = logging.NOTSET,
        formatter: OptionalLoggingFormatter = None,
        loop: OptionalAbstractEventLoop = None,
        **kwargs,
    ):
        """Create new logger."""
        self = cls(name=name, level=level, loop=loop, **kwargs)
        self._stdout_handler = DSAsyncStreamHandler(
            stream=sys.stdout,
            level=level,
            formatter=formatter,
            filter=StdoutFilter()
        )
        self._stderr_handler = DSAsyncStreamHandler(
            stream=sys.stderr,
            level=logging.WARNING,
            formatter=formatter
        )
        self.addHandler(self._stdout_handler)
        self.addHandler(self._stderr_handler)
        return self

    async def set_level(self, level):
        """Set logging level"""
        if self._stdout_handler.writer is not None:
            await self._stdout_handler.flush()
        self._cache.clear()
        super().setLevel(level)
        self._stdout_handler.setLevel(level)
