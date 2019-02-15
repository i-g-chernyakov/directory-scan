# -*- coding: utf-8 -*-

"""
Patch for aiologger.handlers.AsyncStreamHandler

If transport is not pipe compatible (like stdout and stderr in Windows) then
use DSNonFileStreamWriter
"""

import asyncio
from asyncio import StreamWriter

from aiologger.handlers import AsyncStreamHandler

from directory_scan.dsaiologger.stdstreams import (
    DSNonFileStreamWriter,
    is_pipe_transport_compatible,
)


class DSAsyncStreamHandler(AsyncStreamHandler):

    async def _init_writer(self) -> StreamWriter:
        async with self._initialization_lock:
            if not is_pipe_transport_compatible(self.stream):
                self.writer = DSNonFileStreamWriter(self.stream, loop=self.loop)
            else:
                self.loop = asyncio.get_event_loop()
                transport, protocol = await self.loop.connect_write_pipe(
                    protocol_factory=self.protocol_class, pipe=self.stream
                )

                self.writer = StreamWriter(  # type: ignore
                    #  https://github.com/python/typeshed/pull/2719
                    transport=transport,
                    protocol=protocol,
                    reader=None,
                    loop=self.loop,
                )
            return self.writer
