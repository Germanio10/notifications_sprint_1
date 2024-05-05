from pydantic import BaseModel


class User(BaseModel):
    user_id: str | None = None
    role_id: int | str | None = None
