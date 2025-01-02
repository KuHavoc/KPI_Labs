import asyncio
from aiopubsub import Hub


class Subscriber:
    def __init__(self, hub: Hub, topic: str):
        self.hub = hub
        self.topic = topic
        self.subscription = None

    async def subscribe(self):
        self.subscription = await self.hub.subscribe(self.topic, self.on_message)

    async def on_message(self, message: str):
        print(f"Subscriber received message: {message}")

    async def unsubscribe(self):
        if self.subscription:
            await self.hub.unsubscribe(self.subscription)
