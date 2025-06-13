# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictStr
from typing import Any
from typing_extensions import Annotated
from openapi_server.models.problem_details import ProblemDetails
from openapi_server.models.redirect_response import RedirectResponse
from openapi_server.security_api import get_token_oAuth2ClientCredentials

class BaseIndividualNCOFEventSubscriptionTransferApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseIndividualNCOFEventSubscriptionTransferApi.subclasses = BaseIndividualNCOFEventSubscriptionTransferApi.subclasses + (cls,)
    async def delete_ncof_event_subscription_transfer(
        self,
        transferId: Annotated[StrictStr, Field(description="String identifying a request for an analytics subscription transfer to the Nncof_EventsSubscription Service. ")],
    ) -> None:
        ...


    async def update_ncof_event_subscription_transfer(
        self,
        transferId: Annotated[StrictStr, Field(description="String identifying a request for an analytics subscription transfer to the Nncof_EventsSubscription Service ")],
        body: StrictStr,
    ) -> None:
        ...
