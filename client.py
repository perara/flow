import uvloop
import asyncio
import socket
import logger
import inspect


class MCMLSocket(asyncio.Protocol):

    def __init__(self, use_uvloop=True, retry=True, retry_interval=5):

        """Retrieve logger for the class."""
        self.logger = logger.get_logger("MCMLSocket")

        if use_uvloop:
            """Use the uvloop to increase throughput."""
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        self.loop = asyncio.get_event_loop()

        self._cb_on_received_async = []
        self._cb_on_received_sync = []

        self.transport_server_clients = []
        self.transport_server = None
        self.transport_client = None

        self.retry = retry
        self.retry_interval = retry_interval

    def data_received(self, data):
        message = data.decode()

        for cb in self._cb_on_received_sync:
            cb(message)

        for acb in self._cb_on_received_async:
            self.loop.create_task(acb(message))

    def add_on_receive_cb(self, cb):

        if inspect.iscoroutinefunction(cb):
            self._cb_on_received_async.append(cb)
        elif inspect.isfunction(cb):
            self._cb_on_received_sync.append(cb)
        else:
            raise AssertionError("add_on_receive_cb takes in callback which is either async def or def.")

    def connection_made(self, transport):
        self.transport_server_clients.append(transport)
        sock = transport.get_extra_info('socket')
        try:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        except (OSError, NameError):
            pass

    def connection_lost(self, exc):
        print(exc)
        print('The server closed the connection')

        print(dir(self))
        print(self.transpo)

        #self.on_con_lost.set_result(True)

    def listen(self, host, port):
        self.loop.run_until_complete(self.loop.create_server(lambda: self, host, port, backlog=1000))

    def dial(self, host, port):
        self.loop.run_until_complete(self.adial(host, port))

    async def adial(self, host, port):
        try:
            transport, protocol = await self.loop.create_connection(lambda: self, host, port)
            self.transport_client = transport
        except ConnectionRefusedError as e:
            """ Could not connect to server. Retry."""
            self.logger.info("Could not connect to %s:%s. Retrying in %s..." % (host, port, self.retry_interval))
            await asyncio.sleep(self.retry_interval)
            await self.loop.create_task(self.adial(host, port))


    def run_forever(self):
        self.loop.run_forever()

    def send(self, message):
        self.transport_client.write(b'ANNOUNCE EOF')



if __name__ == "__main__":

    count = 0

    async def test(data):
        global count
        count += 1
        #print("async, ", data)

    def test2(data):
        global count
        count += 1
        #print("sync, ", data)

    x = MCMLSocket()
    x.add_on_receive_cb(test)
    x.add_on_receive_cb(test2)
    x.listen("0.0.0.0", 41000)

    x.dial("0.0.0.0", 41000)

    async def benchmark():
        global count

        while True:
            print("Per sec: %s" % count)
            count = 0
            await asyncio.sleep(1.0)

    async def send_spam():
        while True:
            x.send("Lalrl")
            await asyncio.sleep(1)

    x.loop.create_task(send_spam())
    x.loop.create_task(benchmark())

    x.run_forever()
