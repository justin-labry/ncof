# coding: utf-8

import asyncio
from datetime import datetime, timedelta, timezone
import logging
import time
from typing import Optional  # noqa: F401
import uuid


from fastapi import (  # noqa: F401
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    status,
)

from core.nf_client import subscribe_to_nf
from core.nrf_client import get_nf_info

# from core.subscription_manager import SubscriptionManager
# from core.dependency import get_subscription_manager

from core import SubscriptionManager, get_subscription_manager

from openapi_server.models.event_reporting_requirement import EventReportingRequirement
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription
from openapi_server.models.problem_details import ProblemDetails

from config.app_config import app_config

router = APIRouter()


def build_ncof_notification_uri(subscription_id: str) -> str:
    return f"http://{app_config.server_ip}:{app_config.port}/{app_config.notification_prefix}/notifications/{subscription_id}"


# 비동기 작업을 위한 태스크 리스트 생성
async def subscribe_to_nfs(nfs, payload, subscription_id):
    tasks = [
        subscribe_to_nf(
            subscription_id=subscription_id,
            uri=nf.get("uri") or "",
            payload=payload,
        )
        for nf in nfs
    ]
    # 모든 태스크를 병렬로 실행하고 결과를 기다림
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, Exception):
            raise Exception("fail to subscribe")
    return True


logger = logging.getLogger(__name__)
# TIMEZONE: timezone = timezone(timedelta(hours=9))
TIMEZONE = datetime.now().astimezone().tzinfo


def check_subscription(event_subscription):
    if not event_subscription.nf_types:
        raise HTTPException(
            status_code=400,
            detail="No NF types specified in the subscription request",
        )

    current_time = datetime.now(TIMEZONE)

    if event_subscription.extra_report_req is not None:
        end_ts = event_subscription.extra_report_req.end_ts

    if end_ts and current_time >= end_ts:
        logger.info(f"{('종료조건')} - end_ts exceeded ({end_ts})")
        raise HTTPException(
            status_code=400,
            detail=f"Error subscribing: The end time has already passed",
        )


def get_nfs_by_types(nf_types):
    nfs = []
    for nf_type in nf_types or []:
        nf = get_nf_info(nf_type)
        nfs.append(nf)
    return nfs


@router.post(
    "/subscriptions",
    responses={
        201: {
            "description": "Create a new Individual NCOF Event Subscription resource."
        },
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
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=True,
)
async def create_ncof_events_subscription(
    background_tasks: BackgroundTasks,
    subscription: NncofEventsSubscription = Body(None, description=""),
    subscription_manager: SubscriptionManager = Depends(get_subscription_manager),
):
    event_subscription = subscription.event_subscriptions[0]
    try:
        check_subscription(event_subscription)
        nfs = get_nfs_by_types(event_subscription.nf_types)

        # 구독 ID를 생성한다.
        new_subscription_id = str(uuid.uuid4())

        new_nf_events_subscription = subscription.model_copy(deep=True)

        # update the notification URI in the subscription
        new_nf_events_subscription.notification_uri = build_ncof_notification_uri(
            new_subscription_id
        )

        # 보고 주기를 1초로
        if new_nf_events_subscription.event_subscriptions[0].evt_req is not None:
            new_nf_events_subscription.event_subscriptions[0].evt_req.rep_period = 1

        subscription_manager.add_subscription(
            subscription_id=new_subscription_id,
            subscription=subscription,
        )

        background_tasks.add_task(
            subscribe_to_nfs,
            nfs,
            new_nf_events_subscription.model_dump(),
            new_subscription_id,
        )

        return new_subscription_id

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error subscribing: {str(e)}")
    # return await subscription_service.create_ncof_events_subscription(subscription)


@router.get(
    "/subscriptions",
    tags=["NCOF Events Subscriptions"],
    summary="Get all NCOF Events Subscriptions",
)
async def subscriptions(
    subscription_manager: SubscriptionManager = Depends(get_subscription_manager),
):
    return subscription_manager.get_subscriptions()
