import datetime

from pydantic import BaseModel, Field


class CronModel(BaseModel):
    current_time: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
    last_time_update: datetime.datetime
    last_time_send: datetime.datetime | None
    time_of_deletion: datetime.timedelta = datetime.timedelta(days=1)
    time_difference: datetime.timedelta = Field(default=None)

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.last_time_update = data.get('last_time_update')
        self.last_time_send = data.get('last_time_send')
        utc_timezone = datetime.timezone.utc
        if self.last_time_send is not None:
            self.last_time_send = self.last_time_send.astimezone(utc_timezone)
        self.last_update = self.last_update.astimezone(utc_timezone)
        self.time_difference = self.current_time - self.last_update
