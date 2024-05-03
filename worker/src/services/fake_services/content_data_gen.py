from faker import Faker
from models.notification import EventTypeEnum, Notification
from pydantic import BaseModel


class Content(BaseModel):
    subject: str
    text: str
    film: str


class ContentFilmService:
    def __init__(self) -> None:
        self.faker = Faker()

    async def get_content(self, notification: Notification) -> Content:
        fake_text = f'{self.faker.catch_phrase()} {self.faker.word()}'
        film = f'На прошедшей неделе фильм "{fake_text}" в топе просмотров!'

        header = '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><title>Кинотеатр!</title></head><body>'
        footer = '</body></html>'
        if notification.event_type == EventTypeEnum.registered:
            subject = 'Поздравляем с регистрацией!'
            text = (
                header
                + '<h1>Привет {{ name }}! Спасибо за регистрацию в нашем уютном кинотеатре.</h1><p> {{ content }} </p>'
                + footer
            )
        if notification.event_type == EventTypeEnum.recommendations:
            subject = 'Новинки специально для вас!'
            text = (
                header
                + '<h1>Привет {{ name }}! Мы подобрали для вас подборку фильмов.</h1><p> {{ content }} </p>'
                + footer
            )
        if notification.event_type == EventTypeEnum.new_episode:
            subject = 'Новая серия!'
            text = (
                header
                + '<h1>Привет {{ name }}! Долгожданная серия.</h1><p> {{ content }} </p>'
                + footer
            )
        if notification.event_type == EventTypeEnum.like_comment:
            subject = 'Новые лайки'
            text = (
                header
                + '<h1>Привет {{ name }}!</h1><p> Вам поставили {{ content }} лайк(-ов) на {{ content_id }} комментарий </p>'
                + footer
            )
        content = Content(
            subject=subject,
            text=text,
            film=film,
        )
        return content
