import pickle
import uvloop
import asyncio
import socket
import logger
import inspect


class FlowInterface(asyncio.Protocol):

    def __init__(self, loop):
        """Retrieve logger for the class."""
        self.logger = logger.get_logger("FlowInterface")

        self.loop = loop

        """Use the uvloop to increase throughput."""
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        """"""
        self._cb_on_received_async = []
        self._cb_on_received_sync = []

    def add_on_receive(self, cb):

        if inspect.iscoroutinefunction(cb):
            self._cb_on_received_async.append(cb)
        elif inspect.isfunction(cb):
            self._cb_on_received_sync.append(cb)
        else:
            raise AssertionError("add_on_receive_cb takes in callback which is either async def or def.")

    def data_received(self, bytedata):
        message = self.deserialize(bytedata)

        for cb in self._cb_on_received_sync:
            cb(message)

        for acb in self._cb_on_received_async:
            self.loop.create_task(acb(message))

    def connection_made(self, transport):
        sock = transport.get_extra_info('socket')

        try:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except (OSError, NameError):
            pass

    @staticmethod
    def serialize(data):
        return pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def deserialize(bytedata):
        return pickle.loads(bytedata)


class FlowServer(FlowInterface):

    def __init__(self, loop):
        super().__init__(loop)

        self.logger = logger.get_logger("FlowServer")

    def listen(self, host, port):
        self.loop.run_until_complete(self.loop.create_server(lambda: self, host, port, backlog=1000))


class FlowClient(FlowInterface):

    def __init__(self, loop, retry=True, retry_interval=5):
        super().__init__(loop)

        self.logger = logger.get_logger("FlowServer")

        self.retry = retry
        self.retry_interval = retry_interval

        self.transport = None

        self.host = None
        self.port = None

    def dial(self, host, port):
        self.loop.run_until_complete(self.adial(host, port))

    async def adial(self, host, port):
        try:
            self.transport, protocol = await self.loop.create_connection(lambda: self, host, port)
            self.host = host
            self.port = port
        except ConnectionRefusedError as e:
            """ Could not connect to server. Retry."""
            self.logger.info("Could not connect to %s:%s. Retrying in %s seconds..." % (host, port, self.retry_interval))
            await asyncio.sleep(self.retry_interval)
            await self.loop.create_task(self.adial(host, port))

    async def send(self, message):
        if self.transport._conn_lost:
            await asyncio.sleep(.1)
            return

        self.transport.write(self.serialize(message))

    def connection_lost(self, exc):
        self.logger.info("Lost connection to %s:%s. Reconnecting..." % (self.host, self.host))
        self.loop.create_task(self.adial(self.host, self.port))


class Flow:

    def __init__(self, loop=None, retry=True, retry_interval=5):

        if not loop:
            loop = asyncio.new_event_loop()

        self.loop = loop

        self.server = FlowServer(loop=loop)
        self.client = FlowClient(loop=loop, retry=True, retry_interval=5)

    def run_forever(self):
        self.loop.run_forever()

