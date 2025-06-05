# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import StrictStr
from typing import Any
from openapi_server.models.problem_details import ProblemDetails
from openapi_server.security_api import get_token_oAuth2ClientCredentials

class BaseNCOFEventSubscriptionTransfersApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseNCOFEventSubscriptionTransfersApi.subclasses = BaseNCOFEventSubscriptionTransfersApi.subclasses + (cls,)
    async def create_ncof_event_subscription_transfer(
        self,
        body: StrictStr,
    ) -> None:
        ...
