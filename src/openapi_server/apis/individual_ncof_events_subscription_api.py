# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.individual_ncof_events_subscription_api_base import (
    BaseIndividualNCOFEventsSubscriptionApi,
)
from openapi_server.apis.ncof_events_subscriptions_api_base import (
    BaseNCOFEventsSubscriptionsApi,
)
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.impl.dependency import get_subscription_service
from openapi_server.impl.events_subscriptions_impl import SubscriptionNotFoundError
from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr
from typing import Any
from typing_extensions import Annotated
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription
from openapi_server.models.problem_details import ProblemDetails
from openapi_server.models.redirect_response import RedirectResponse
from openapi_server.security_api import get_token_oAuth2ClientCredentials

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/subscriptions/{subscription_id}",
    responses={
        204: {
            "description": "No Content. The Individual NCOF Event Subscription resource matching the subscriptionId was deleted. "
        },
        307: {"model": RedirectResponse, "description": "Temporary Redirect"},
        308: {"model": RedirectResponse, "description": "Permanent Redirect"},
        400: {"model": ProblemDetails, "description": "Bad request"},
        401: {"model": ProblemDetails, "description": "Unauthorized"},
        403: {"model": ProblemDetails, "description": "Forbidden"},
        404: {"model": ProblemDetails, "description": "Not Found"},
        429: {"model": ProblemDetails, "description": "Too Many Requests"},
        500: {"model": ProblemDetails, "description": "Internal Server Error"},
        501: {"model": ProblemDetails, "description": "Not Implemented"},
        502: {"model": ProblemDetails, "description": "Bad Gateway"},
        503: {"model": ProblemDetails, "description": "Service Unavailable"},
        200: {"description": "Generic Error"},
    },
    tags=["Individual NCOF Events Subscription"],
    summary="Delete an existing Individual NCOF Events Subscription",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model_by_alias=True,
)
async def delete_ncof_events_subscription(
    subscription_id: Annotated[
        StrictStr,
        Field(
            description="String identifying a subscription to the Nncof_EventsSubscription Service"
        ),
    ] = Path(
        ...,
        description="String identifying a subscription to the Nncof_EventsSubscription Service",
    ),
    subscription_service: BaseIndividualNCOFEventsSubscriptionApi = Depends(
        get_subscription_service
    ),
):
    if not BaseIndividualNCOFEventsSubscriptionApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return (
        await subscription_service.delete_ncof_events_subscription(subscription_id),
    )
    # try:
    # except SubscriptionNotFoundError:
    #     # raise HTTPException(status_code=404)
    #     pass
    # except:
    #     raise HTTPException(status_code=500, detail="Server error")


@router.put(
    "/subscriptions/{subscription_id}",
    responses={
        200: {
            "model": NncofEventsSubscription,
            "description": "The Individual NCOF Event Subscription resource was modified successfully and a representation of that resource is returned. ",
        },
        204: {
            "description": "The Individual NCOF Event Subscription resource was modified successfully."
        },
        307: {"model": RedirectResponse, "description": "Temporary Redirect"},
        308: {"model": RedirectResponse, "description": "Permanent Redirect"},
        400: {"model": ProblemDetails, "description": "Bad request"},
        401: {"model": ProblemDetails, "description": "Unauthorized"},
        403: {"model": ProblemDetails, "description": "Forbidden"},
        404: {"model": ProblemDetails, "description": "Not Found"},
        411: {"model": ProblemDetails, "description": "Length Required"},
        413: {"model": ProblemDetails, "description": "Content Too Large"},
        415: {"model": ProblemDetails, "description": "Unsupported Media Type"},
        429: {"model": ProblemDetails, "description": "Too Many Requests"},
        500: {"model": ProblemDetails, "description": "Internal Server Error"},
        501: {"model": ProblemDetails, "description": "Not Implemented"},
        502: {"model": ProblemDetails, "description": "Bad Gateway"},
        503: {"model": ProblemDetails, "description": "Service Unavailable"},
        200: {"description": "Generic Error"},
    },
    tags=["Individual NCOF Events Subscription"],
    summary="Update an existing Individual NCOF Events Subscription",
    status_code=status.HTTP_200_OK,
    response_model_by_alias=True,
)
async def update_ncof_events_subscription(
    subscription_id: Annotated[
        StrictStr,
        Field(
            description="String identifying a subscription to the Nncof_EventsSubscription Service."
        ),
    ] = Path(
        ...,
        description="String identifying a subscription to the Nncof_EventsSubscription Service.",
    ),
    subscription: NncofEventsSubscription = Body(None, description=""),
    subscription_service: BaseIndividualNCOFEventsSubscriptionApi = Depends(
        get_subscription_service
    ),
):
    if not BaseIndividualNCOFEventsSubscriptionApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await subscription_service.update_ncof_events_subscription(
        subscription_id, subscription
    )
