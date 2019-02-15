# -*- coding: utf-8 -*-

import io
import json
import logging
import sys

import pytest
from aiologger.formatters.json import JsonFormatter

from directory_scan.dsaiologger import DSJsonLogger


@pytest.fixture
async def make_logger():
    """Make logger and shutdown after using"""
    created_logger = []

    def _make_logger(
        name="dsjsonlogger",
        level=logging.NOTSET,
        serializer=json.dumps,
        flatten=False,
        serializer_kwargs=None,
        extra=None,
        exclude_fields=None,
        loop=None,
        tz=None,
        formatter=None,
    ):
        _logger = DSJsonLogger.with_default_handlers(
            name=name,
            level=level,
            serializer=serializer,
            flatten=flatten,
            serializer_kwargs=serializer_kwargs,
            extra=extra,
            exclude_fields=exclude_fields,
            loop=loop,
            tz=tz,
            formatter=formatter,
        )
        created_logger.append(_logger)
        return _logger

    yield _make_logger

    await created_logger.pop().shutdown()


@pytest.mark.asyncio
@pytest.mark.parametrize("level,formatter", [
    (logging.INFO, None),
    (logging.INFO, JsonFormatter()),
])
async def test_dsjsonlogger(monkeypatch, make_logger, level, formatter):
    virtual_stdout = io.StringIO()
    virtual_stderr = io.StringIO()
    with monkeypatch.context() as monkey:
        monkey.setattr(sys, "stdout", virtual_stdout)
        monkey.setattr(sys, "stderr", virtual_stderr)

        logger = make_logger(
            level=level,
            formatter=formatter,
        )

        await logger.info('abc')

        result = json.loads(virtual_stdout.getvalue())

        assert result
        assert result['msg'] == 'abc'


@pytest.mark.asyncio
async def test_dsjsonlogger_set_level():
    logger = DSJsonLogger.with_default_handlers(level=logging.INFO)

    assert logger.level == logging.INFO

    await logger.set_level(logging.DEBUG)

    assert logger.level == logging.DEBUG
