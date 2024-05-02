import uuid

from faker import Faker
from pydantic import BaseModel, EmailStr


class EmailData(BaseModel):
    name: str
    email: EmailStr


class EmailDataGenerator:
    def __init__(self) -> None:
        self.faker = Faker()

    async def generate_email_data(self, user_id: uuid.UUID) -> EmailData:
        name = self.faker.name()
        email = self.faker.email()
        return EmailData(name=name, email=email)
