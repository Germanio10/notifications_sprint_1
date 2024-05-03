from abc import ABC, abstractmethod
from typing import Callable


class AbstractBroker(ABC):
    async def close(self) -> None:
        pass

    @abstractmethod
    async def create_queue(self) -> None:
        pass

    @abstractmethod
    async def consume(self, queue: str, callback: Callable) -> None:
        pass

    @abstractmethod
    async def send_to_broker(self, body: bytes, exchange: str = '') -> None:
        pass


broker: AbstractBroker | None = None


async def get_broker() -> AbstractBroker:
    await broker.create_queue()
    return broker
