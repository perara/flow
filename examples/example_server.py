import asyncio

from client import MCMLSocket

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

    x.loop.create_task(benchmark())

    x.run_forever()
