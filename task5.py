import asyncio
from aiopubsub import Hub
from publisher import Publisher
from subscriber import Subscriber


async def main():
    hub = Hub()
    topic = "my_topic"

    publisher = Publisher(hub, topic)
    subscriber1 = Subscriber(hub, topic)
    subscriber2 = Subscriber(hub, topic)

    await subscriber1.subscribe()
    await subscriber2.subscribe()

    await publisher.publish("Hello from publisher!")
    await asyncio.sleep(0.1)
    await publisher.publish("Another message!")
    await asyncio.sleep(0.1)

    await subscriber1.unsubscribe()
    await publisher.publish("Message after unsubscribe")
    await asyncio.sleep(0.1)

    await subscriber2.unsubscribe()


if __name__ == "__main__":
    asyncio.run(main())
