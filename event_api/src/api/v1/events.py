from http import HTTPStatus

from fastapi import APIRouter, Body, Depends
from models.notifications import Event
from models.response_model import ResponseNotification, ResponseTemplate
from models.templates import Template
from service.notifications import Notifications, get_notification_service

events_router = APIRouter()


@events_router.post(
    '/',
    description='Создание уведомления',
    status_code=HTTPStatus.CREATED,
    response_model=ResponseNotification,
)
async def create_notification(
    event: Event = Body(), notification: Notifications = Depends(get_notification_service)
):
    return await notification.create_notification(event)


@events_router.post(
    '/template',
    description='Создание шаблона',
    status_code=HTTPStatus.CREATED,
    response_model=ResponseTemplate,
)
async def create(
    template: Template = Body(),
    notification: Notifications = Depends(get_notification_service),
):
    return await notification.create_template(template)
