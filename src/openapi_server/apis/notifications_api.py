# coding: utf-8

import logging

from typing_extensions import Annotated

from pydantic import Field, StrictStr

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Path,
    status,
)

from core.subscription_manager import SubscriptionManager
from core.dependency import get_subscription_manager

from openapi_server.models.event_notification import EventNotification

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/notifications/{subscription_id}",
    responses={
        201: {"description": "notification sent"},
        400: {"description": "invalid input, object invalid"},
        409: {"description": "an existing item already exists"},
    },
    tags=["NCOF Events Notifications"],
    summary="Create a new Individual NCOF Events Notification",
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=True,
)
async def create_nwdaf_events_notification(
    subscription_id: Annotated[StrictStr, Field()] = Path(),
    subscription_manager: SubscriptionManager = Depends(get_subscription_manager),
    event_notification: EventNotification = Body(
        None, description="Event notification containing NF load level information"
    ),
):
    """외부 서버로부터 알림 수신"""

    if not event_notification.nf_load_level_infos:
        raise HTTPException(
            status_code=400,
            detail="No load level information provided in the notification",
        )

    handler = subscription_manager.get_handler(subscription_id)

    if not handler:
        raise HTTPException(status_code=404, detail="구독 ID를 찾을 수 없음")

    for load in event_notification.nf_load_level_infos:
        handler.add_load_info(load)

    return None
