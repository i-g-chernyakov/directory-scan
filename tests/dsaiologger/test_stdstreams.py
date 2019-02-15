# -*- coding: utf-8 -*-

import io
import os
import sys

import pytest

from directory_scan.dsaiologger.stdstreams import (
    DSNonFileStreamReader,
    DSNonFileStreamWriter,
    is_pipe_transport_compatible,
)


@pytest.mark.skipif('sys.platform != "win32"')
def test_is_pipe_transport_compatible_win32():
    assert not is_pipe_transport_compatible(sys.stdout)
    assert not is_pipe_transport_compatible(sys.stderr)


@pytest.mark.skipif('sys.platform == "win32"')
def test_is_pipe_transport_compatible():
    r, w = os.pipe()
    stdin = open(r)
    stdout = open(w, 'w')
    stderr = open(w, 'w')

    assert is_pipe_transport_compatible(stdin)
    assert is_pipe_transport_compatible(stdout)
    assert is_pipe_transport_compatible(stderr)


@pytest.mark.asyncio
async def test_file_stream_writer_write_str():
    std_stream = io.StringIO()
    writer = DSNonFileStreamWriter(std_stream)
    writer.write('abc')
    await writer.drain()
    writer.close()

    assert std_stream.getvalue() == 'abc'


@pytest.mark.asyncio
async def test_file_stream_writer_write_bytes():
    std_stream = io.StringIO()
    writer = DSNonFileStreamWriter(std_stream)
    writer.write(b'abc')
    await writer.drain()
    writer.close()

    assert std_stream.getvalue() == 'abc'


@pytest.mark.asyncio
async def test_file_stream_writer_with_loop(event_loop):
    std_stream = io.StringIO()
    writer = DSNonFileStreamWriter(std_stream, loop=event_loop)
    writer.write('abc')
    await writer.drain()

    assert std_stream.getvalue() == 'abc'


@pytest.mark.asyncio
async def test_file_stream_writer_stream_without_flash(event_loop):

    class PseudoStream(object):
        def __init__(self):
            self._buffer = ''

        def write(self, data):
            self._buffer = data

    pseudo_stream = PseudoStream()
    writer = DSNonFileStreamWriter(pseudo_stream, loop=event_loop)
    writer.write('abc')
    await writer.drain()

    assert pseudo_stream._buffer == 'abc'


@pytest.mark.asyncio
async def test_file_stream_reader(event_loop):
    std_stream = io.StringIO('abc\ndef\n')
    reader = DSNonFileStreamReader(std_stream, loop=event_loop)

    data = await reader.read(n=1)

    assert data == b'a'


@pytest.mark.asyncio
async def test_file_stream_reader_readline(event_loop):
    std_stream = io.StringIO('abc\ndef\n')
    reader = DSNonFileStreamReader(std_stream)

    data = await reader.readline()

    assert data == b'abc\n'

    await reader.readline()
    await reader.readline()

    assert reader.at_eof()


@pytest.mark.asyncio
async def test_file_stream_reader_readbytes(event_loop):
    std_stream = io.BytesIO(b'abc\n')
    reader = DSNonFileStreamReader(std_stream)

    byt = await reader.read(1)

    assert byt == b'a'

    data = await reader.readline()

    assert data == b'bc\n'

    await reader.readline()

    assert reader.at_eof()
