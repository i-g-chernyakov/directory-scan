# -*- coding: utf-8 -*-

"""
Patch for `aiologger.loggers.JsonLogger`

Replace parent class with DSLogger
"""

import json
import logging
from asyncio import AbstractEventLoop
from datetime import timezone
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from aiologger.formatters.json import ExtendedJsonFormatter
from aiologger.logger import _Caller
from aiologger.loggers.json import LogRecord

from directory_scan.dsaiologger.logger import DSLogger


class DSJsonLogger(DSLogger):
    def __init__(
        self,
        name: str = "dsjsonlogger",
        level: int = logging.DEBUG,
        flatten: bool = False,
        serializer_kwargs: Dict = None,
        extra: Dict = None,
        loop: AbstractEventLoop = None,
    ) -> None:
        super().__init__(name=name, level=level, loop=loop)

        self.flatten = flatten

        if serializer_kwargs is None:
            serializer_kwargs = {}
        self.serializer_kwargs = serializer_kwargs

        if extra is None:
            extra = {}
        self.extra = extra

    @classmethod
    def with_default_handlers(  # type: ignore
        cls,
        *,
        name: str = "dsjsonlogger",
        level: int = logging.NOTSET,
        serializer: Callable[..., str] = json.dumps,
        flatten: bool = False,
        serializer_kwargs: Dict = None,
        extra: Dict = None,
        exclude_fields: Iterable[str] = None,
        loop: AbstractEventLoop = None,
        tz: timezone = None,
        formatter: Optional[logging.Formatter] = None,
    ):
        if formatter is None:
            formatter = ExtendedJsonFormatter(
                serializer=serializer, exclude_fields=exclude_fields, tz=tz
            )
        return super(DSJsonLogger, cls).with_default_handlers(
            name=name,
            level=level,
            loop=loop,
            flatten=flatten,
            serializer_kwargs=serializer_kwargs,
            extra=extra,
            formatter=formatter,
        )

    async def _log(  # type: ignore
        self,
        level: int,
        msg: Any,
        args: Tuple,
        exc_info=None,
        extra: Dict = None,
        stack_info=False,
        flatten: bool = False,
        serializer_kwargs: Dict = None,
        caller: _Caller = None,
    ):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.

        Overwritten to properly handle log methods kwargs
        """
        sinfo = None
        if caller:
            fn, lno, func, sinfo = caller
        else:  # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info and isinstance(exc_info, BaseException):
            exc_info = (type(exc_info), exc_info, exc_info.__traceback__)

        joined_extra = {}
        joined_extra.update(self.extra)

        if extra:
            joined_extra.update(extra)

        record = LogRecord(
            name=self.name,
            level=level,
            pathname=fn,
            lineno=lno,
            msg=msg,
            args=args,
            exc_info=exc_info,
            func=func,
            sinfo=sinfo,
            extra=joined_extra,
            flatten=flatten or self.flatten,
            serializer_kwargs=serializer_kwargs or self.serializer_kwargs,
        )
        await self.handle(record)

    async def set_level(self, level):
        await super().set_level(level)
