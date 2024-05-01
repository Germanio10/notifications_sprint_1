import uuid
from http import HTTPStatus

from fastapi import HTTPException
from jinja2 import Environment, TemplateSyntaxError
from models.notifications import EventTypeEnum, NotificationTypeEnum
from pydantic import BaseModel, Field, field_validator, ValidationInfo


class Template(BaseModel):
    template_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    event_type: EventTypeEnum | None
    type: NotificationTypeEnum = NotificationTypeEnum.email
    subject: str | None
    content_data: str

    @field_validator('subject')
    def validate_subject(cls, subject, info: ValidationInfo) -> str:
        if info.data.get('type') == NotificationTypeEnum.email and not subject:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Subject field is required for email type',
            )

        if subject:
            try:
                Environment(autoescape=True).parse(subject)
            except TemplateSyntaxError as err:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=f'Invalid template subject: {err}',
                )

        return subject

    @field_validator('content_data')
    def validate_content(cls, content_data) -> str:
        try:
            Environment(autoescape=True).parse(content_data)
        except TemplateSyntaxError as err:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f'Invalid template content: {err}',
            )

        return content_data


class Example(BaseModel):
    test: int


class TemplateError(Exception):
    """Класс для ошибок шаблона."""
