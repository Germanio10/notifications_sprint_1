import uuid

from models.notification import EventTypeEnum, NotificationTypeEnum
from pydantic import field_validator, BaseModel, ValidationInfo


class Template(BaseModel):
    template_id: uuid.UUID
    event_type: EventTypeEnum | None
    type: NotificationTypeEnum = NotificationTypeEnum.email
    subject: str | None
    content_data: str

    @field_validator('subject')
    def validate_subject(cls, subject, info: ValidationInfo):
        if info.data.get('type') == NotificationTypeEnum.email and subject is None:
            raise ValueError('Subject required for type email')
        return subject
