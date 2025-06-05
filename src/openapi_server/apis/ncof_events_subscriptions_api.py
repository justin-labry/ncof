# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.ncof_events_subscriptions_api_base import BaseNCOFEventsSubscriptionsApi
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
from openapi_server.models.extra_models import TokenModel  # noqa: F401
from typing import Any
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription
from openapi_server.models.problem_details import ProblemDetails
from openapi_server.security_api import get_token_oAuth2ClientCredentials

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)

@router.post(
    "/subscriptions",
    responses={
        201: {"description": "Create a new Individual NCOF Event Subscription resource."},
        400: {"model": ProblemDetails, "description": "Bad request"},
        401: {"model": ProblemDetails, "description": "Unauthorized"},
        403: {"model": ProblemDetails, "description": "Forbidden"},
        404: {"model": ProblemDetails, "description": "Not Found"},
        411: {"model": ProblemDetails, "description": "Length Required"},
        413: {"model": ProblemDetails, "description": "Content Too Large"},
        415: {"model": ProblemDetails, "description": "Unsupported Media Type"},
        429: {"model": ProblemDetails, "description": "Too Many Requests"},
        500: {"model": ProblemDetails, "description": "Internal Server Error"},
        502: {"model": ProblemDetails, "description": "Bad Gateway"},
        503: {"model": ProblemDetails, "description": "Service Unavailable"},
        200: {"description": "Generic Error"},
    },
    tags=["NCOF Events Subscriptions"],
    summary="Create a new Individual NCOF Events Subscription",
    response_model_by_alias=True,
)
async def create_ncof_events_subscription(
    nncof_events_subscription: NncofEventsSubscription = Body(None, description=""),
    subscription_service: BaseNCOFEventsSubscriptionsApi = Depends(
        get_subscription_service
    ),
    token_oAuth2ClientCredentials: TokenModel = Security(
        get_token_oAuth2ClientCredentials, scopes=["nncof-eventssubscription"]
    ),
):
    if not BaseNCOFEventsSubscriptionsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    subscription_id = await subscription_service.create_ncof_events_subscription(nncof_events_subscription)
    return Response(subscription_id, status_code=status.HTTP_201_CREATED)
