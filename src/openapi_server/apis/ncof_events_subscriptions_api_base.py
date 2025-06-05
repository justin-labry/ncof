# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription
from openapi_server.models.problem_details import ProblemDetails
from openapi_server.security_api import get_token_oAuth2ClientCredentials

class BaseNCOFEventsSubscriptionsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseNCOFEventsSubscriptionsApi.subclasses = BaseNCOFEventsSubscriptionsApi.subclasses + (cls,)
    async def create_ncof_events_subscription(
        self,
        nncof_events_subscription: NncofEventsSubscription,
    ) -> str:
        ...
