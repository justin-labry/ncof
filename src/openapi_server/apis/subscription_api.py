# coding: utf-8
from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    status,
)

from typing_extensions import Annotated

from pydantic import Field, StrictStr

from core.dependency import get_subscription_manager
from core.subscription_manager import SubscriptionManager

from openapi_server.models.nncof_events_subscription import NncofEventsSubscription
from openapi_server.models.problem_details import ProblemDetails
from openapi_server.models.redirect_response import RedirectResponse

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


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
    tags=["NCOF Events Subscriptions"],
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
    subscription_manager: SubscriptionManager = Depends(get_subscription_manager),
):

    try:
        if subscription_manager.remove_subscription(subscription_id):
            return None
    except:
        raise HTTPException(500, "Internal server error")


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
    tags=["NCOF Events Subscriptions"],
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
):
    raise HTTPException(status_code=500, detail="Not implemented")
