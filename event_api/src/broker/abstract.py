"""Описание интерфейса для работы с брокером сообщений."""

import abc


class AbstractBroker(abc.ABC):
    """Абстрактный класс для работы с брокером сообщений."""

    @abc.abstractmethod
    async def declare_queue(self, queue_name: str):
        """Создание очередей."""

    @abc.abstractmethod
    async def send_to_broker(self, routing_key: str, body: bytes, exchange: str = ''):
        """Публикация сообщения в очередь брокера."""


broker: AbstractBroker | None = None


def get_broker() -> AbstractBroker | None:
    return broker

