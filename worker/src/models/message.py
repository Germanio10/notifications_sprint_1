from pydantic import BaseModel, EmailStr


class EmailModel(BaseModel):
    to_email: EmailStr
    subject: str
    body: str


class WsMessage(BaseModel):
    type: str
    message: dict


class MailMessageError(Exception):
    pass
