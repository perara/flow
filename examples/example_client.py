import asyncio

from client import Flow

if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    async def func():
        x = Flow(loop=loop)
        await x.client.adial("0.0.0.0", 41000)

        while True:
            await x.client.send("ewrgwe+rogkweåprigjewåprijgweåoprjgwåpeorjgåpowerjg")

    loop.create_task(func())

    loop.run_forever()