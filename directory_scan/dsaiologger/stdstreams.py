# -*- coding: utf-8 -*-

"""
Provide asynchronous writers for stdout and stderr

Use code from [aioconsole][https://github.com/vxgmichel/aioconsole],
stream.py
"""

import asyncio
import os
import platform
import stat
from typing import Union

StringOfBytes = Union[str, bytes]


def is_pipe_transport_compatible(pipe) -> bool:
    """Check is pipe compatible with transport

    Taken from aioconsole/stream.py
    """
    if platform.system() == 'Windows':
        return False
    try:
        file_no = pipe.fileno()
    except OSError:
        return False
    mode = os.fstat(file_no).st_mode
    is_char = stat.S_ISCHR(mode)
    is_fifo = stat.S_ISFIFO(mode)
    is_socket = stat.S_ISSOCK(mode)
    if not (is_char or is_fifo or is_socket):
        return False
    return True


class DSNonFileStreamReader(object):
    """ Asynchronous reader from stream

    Based on aioconsole.stream.NonFileStreamReader
    Use run_in_executor
    """

    def __init__(
        self,
        stream,
        *,
        loop: asyncio.AbstractEventLoop = None
    ) -> None:
        """Create async stream reader."""
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.stream = stream
        self.eof = False

    def at_eof(self) -> bool:
        """Is it at eof."""
        return self.eof

    async def readline(self) -> bytes:
        """Async read a line from stream."""
        data = await self.loop.run_in_executor(None, self.stream.readline)
        if isinstance(data, str):
            data = data.encode()
        self.eof = not data
        return data

    async def read(self, n: int = -1) -> bytes:
        """Async read n bytes from stream."""
        data = await self.loop.run_in_executor(None, self.stream.read, n)
        if isinstance(data, str):
            data = data.encode()
        self.eof = not data
        return data


class DSNonFileStreamWriter(object):
    """ Asynchronous writer to stream

    Based on aioconsole.stream.NonFileStreamWriter
    Use run_in_executor
    """

    def __init__(
        self,
        stream,
        *,
        loop: asyncio.AbstractEventLoop = None
    ) -> None:
        """Create async stream writer."""
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        self.stream = stream

    def write(self, data: StringOfBytes) -> None:
        """Write data to stream."""
        if isinstance(data, bytes):
            data = data.decode()
        self.stream.write(data)

    async def drain(self) -> None:
        """Async flush stream in loop."""
        if hasattr(self.stream, 'flush'):
            await self.loop.run_in_executor(None, self.stream.flush)
        else:
            pass

    def close(self):
        pass
