# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any
from openapi_server.models.event_notification import EventNotification


class BaseNWDAFEventsNotificationsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseNWDAFEventsNotificationsApi.subclasses = (
            BaseNWDAFEventsNotificationsApi.subclasses + (cls,)
        )

    async def create_nwdaf_events_notification(
        self,
        subscription_id: str,
        event_notification: EventNotification,
    ) -> None: ...
