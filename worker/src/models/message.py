from pydantic import BaseModel, EmailStr


class EmailModel(BaseModel):
    to_email: EmailStr
    subject: str
    body: str


class MailMessageError(Exception):
    pass
