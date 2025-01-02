import asyncio
from aiopubsub import Hub


class Publisher:
    def __init__(self, hub: Hub, topic: str):
        self.hub = hub
        self.topic = topic

    async def publish(self, message: str):
        await self.hub.publish(self.topic, message)
