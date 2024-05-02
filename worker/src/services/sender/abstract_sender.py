from abc import ABC, abstractmethod

from models.message import EmailModel


class SenderError(Exception):
    pass


class AbstractSender(ABC):
    pass

    @abstractmethod
    async def send(self, msg: EmailModel) -> None:
        pass
