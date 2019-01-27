import asyncio

from client import Flow

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

    async def benchmark():
        global count

        while True:
            print("Per sec: %s" % count)
            count = 0
            await asyncio.sleep(1.0)


    x = Flow()
    #x.server.add_on_receive(test)
    x.server.add_on_receive(test2)
    x.server.listen("0.0.0.0", 41000)
    x.loop.create_task(benchmark())

    x.run_forever()
