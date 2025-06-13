# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.subscription_transfer_api_base import (
    BaseIndividualNCOFEventSubscriptionTransferApi,
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

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictStr
from typing import Any
from typing_extensions import Annotated
from openapi_server.models.problem_details import ProblemDetails
from openapi_server.models.redirect_response import RedirectResponse
from openapi_server.security_api import get_token_oAuth2ClientCredentials

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/transfers/{transferId}",
    responses={
        204: {
            "description": "No Content. The Individual NCOF Event Subscription Transfer resource matching the transferId was deleted. "
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
    tags=["NCOF Event Subscription Transfers"],
    summary="Delete an existing Individual NCOF Event Subscription Transfer",
    response_model_by_alias=True,
)
async def delete_ncof_event_subscription_transfer(
    transferId: Annotated[
        StrictStr,
        Field(
            description="String identifying a request for an analytics subscription transfer to the Nncof_EventsSubscription Service. "
        ),
    ] = Path(
        ...,
        description="String identifying a request for an analytics subscription transfer to the Nncof_EventsSubscription Service. ",
    ),
    token_oAuth2ClientCredentials: TokenModel = Security(
        get_token_oAuth2ClientCredentials, scopes=["nncof-eventssubscription"]
    ),
) -> None:
    if not BaseIndividualNCOFEventSubscriptionTransferApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseIndividualNCOFEventSubscriptionTransferApi.subclasses[
        0
    ]().delete_ncof_event_subscription_transfer(transferId)


@router.put(
    "/transfers/{transferId}",
    responses={
        204: {
            "description": "The Individual NCOF Event Subscription Transfer resource was modified successfully. "
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
    tags=["NCOF Event Subscription Transfers"],
    summary="Update an existing Individual NCOF Event Subscription Transfer",
    response_model_by_alias=True,
)
async def update_ncof_event_subscription_transfer(
    transferId: Annotated[
        StrictStr,
        Field(
            description="String identifying a request for an analytics subscription transfer to the Nncof_EventsSubscription Service "
        ),
    ] = Path(
        ...,
        description="String identifying a request for an analytics subscription transfer to the Nncof_EventsSubscription Service ",
    ),
    body: StrictStr = Body(None, description=""),
    token_oAuth2ClientCredentials: TokenModel = Security(
        get_token_oAuth2ClientCredentials, scopes=["nncof-eventssubscription"]
    ),
) -> None:
    if not BaseIndividualNCOFEventSubscriptionTransferApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseIndividualNCOFEventSubscriptionTransferApi.subclasses[
        0
    ]().update_ncof_event_subscription_transfer(transferId, body)
