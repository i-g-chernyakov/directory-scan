# -*- coding: utf-8 -*-

import io
import logging
import sys

import pytest

from directory_scan.dsaiologger import (
    DSJsonLogger,
    DSLogger,
    get_logger,
    remove_logger,
    set_logger,
)


@pytest.mark.asyncio
async def test_set_logger():
    logger = DSLogger.with_default_handlers()
    set_logger(logger)
    p_logger = get_logger()

    assert p_logger() == logger

    remove_logger()

    assert isinstance(p_logger(), DSJsonLogger)

    remove_logger()
    await logger.shutdown()


@pytest.mark.asyncio
async def test_dslogger_set_level():
    logger = DSLogger.with_default_handlers(level=logging.INFO)

    assert logger.level == logging.INFO

    await logger.set_level(logging.DEBUG)

    assert logger.level == logging.DEBUG


@pytest.mark.asyncio
async def test_dslogger_check_setting_level(monkeypatch):
    virtual_stdout = io.StringIO()
    virtual_stderr = io.StringIO()

    with monkeypatch.context() as monkey:
        monkey.setattr(sys, "stdout", virtual_stdout)
        monkey.setattr(sys, "stderr", virtual_stderr)

        logger = DSLogger.with_default_handlers(level=logging.INFO)

        await logger.info('abc')

        assert virtual_stdout.getvalue() == 'abc\n'

        await logger.set_level(logging.DEBUG)

        await logger.debug('def')

        assert virtual_stdout.getvalue() == 'abc\ndef\n'
