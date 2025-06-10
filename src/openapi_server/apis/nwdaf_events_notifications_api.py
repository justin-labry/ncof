# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil
from typing_extensions import Annotated

from pydantic import Field, StrictStr

from openapi_server.apis.nwdaf_events_notifications_api_base import (
    BaseNWDAFEventsNotificationsApi,
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
from typing import Any
from openapi_server.models.event_notification import EventNotification
from openapi_server.impl.dependency import get_notification_service

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/notifications/{subscription_id}",
    responses={
        201: {"description": "notification sent"},
        400: {"description": "invalid input, object invalid"},
        409: {"description": "an existing item already exists"},
    },
    tags=["NWDAF Events Notifications"],
    summary="Create a new Individual NCOF Events Notification",
    response_model_by_alias=True,
)
async def create_nwdaf_events_notification(
    subscription_id: Annotated[
        StrictStr,
        Field(),
    ] = Path(),
    notification_service: BaseNWDAFEventsNotificationsApi = Depends(
        get_notification_service
    ),
    event_notification: EventNotification = Body(None, description=""),
) -> None:
    if not BaseNWDAFEventsNotificationsApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")

    return await notification_service.create_nwdaf_events_notification(
        subscription_id, event_notification
    )
