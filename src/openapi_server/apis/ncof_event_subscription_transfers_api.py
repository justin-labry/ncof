# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.ncof_event_subscription_transfers_api_base import BaseNCOFEventSubscriptionTransfersApi
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

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import StrictStr
from typing import Any
from openapi_server.models.problem_details import ProblemDetails
from openapi_server.security_api import get_token_oAuth2ClientCredentials

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/transfers",
    responses={
        201: {"description": "Create a new Individual NCOF Event Subscription Transfer resource."},
        204: {"description": "No Content. The receipt of the information about analytics subscription(s) that are requested to be transferred and the ability to handle this information (e.g. execute the steps required to transfer an analytics subscription directly) is confirmed. "},
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
    tags=["NCOF Event Subscription Transfers"],
    summary="Provide information about requested analytics subscriptions transfer and potentially create a new Individual NCOF Event Subscription Transfer resource.",
    response_model_by_alias=True,
)
async def create_ncof_event_subscription_transfer(
    body: StrictStr = Body(None, description=""),
    token_oAuth2ClientCredentials: TokenModel = Security(
        get_token_oAuth2ClientCredentials, scopes=["nncof-eventssubscription"]
    ),
) -> None:
    if not BaseNCOFEventSubscriptionTransfersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseNCOFEventSubscriptionTransfersApi.subclasses[0]().create_ncof_event_subscription_transfer(body)
