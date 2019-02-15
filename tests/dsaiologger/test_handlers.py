# -*- coding: utf-8 -*-

import io
import logging
from logging import LogRecord

import pytest

from directory_scan.dsaiologger.handlers import DSAsyncStreamHandler


@pytest.mark.asyncio
async def test_dsasyncsreamhandler():
    stream = io.StringIO()

    handler = DSAsyncStreamHandler(stream=stream, level=logging.INFO)

    assert handler.writer is None

    log_record = LogRecord(
        name='name',
        level=logging.INFO,
        pathname='',
        lineno=1,
        msg='abc',
        args=(),
        exc_info=None,
    )
    await handler.emit(log_record)

    assert handler.writer is not None
