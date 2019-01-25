import asyncio

from client import MCMLSocket

if __name__ == "__main__":

    async def func():
        x = MCMLSocket()
        await x.adial("0.0.0.0", 41000)

        while True:
            x.send("Lalrl")
            await asyncio.sleep(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(func())