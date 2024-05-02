from abc import ABC, abstractmethod


class AbstractBroker(ABC):
    @abstractmethod
    async def create_queue(self, queue_name: str):
        pass

    @abstractmethod
    async def send_to_broker(self, routing_key: str, body: bytes, exchange: str = ''):
        pass


broker: AbstractBroker | None = None


async def get_broker() -> AbstractBroker:
    await broker.create_queue()
    return broker
