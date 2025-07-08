# coding: utf-8

import asyncio
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

    print(event_subscription.nf_load_lvl_thds[0].avg_traffic_rate)

    extra_report_req: Optional[EventReportingRequirement] = getattr(
        event_subscription, "extra_report_req", None
    )

    if not event_subscription.nf_types:
        raise HTTPException(
            status_code=400,
            detail="No NF types specified in the subscription request",
        )

    nfs = []
    for nf_type in event_subscription.nf_types:
        nf_info = get_nf_info(nf_type)
        nfs.append(nf_info)
        if not nf_info:
            raise HTTPException(
                status_code=404,
                detail=f"NF type {nf_type} not found in NRF",
            )

    try:
        # 구독 ID를 생성한다.
        subscription_id = str(uuid.uuid4())

        new_nf_events_subscription = subscription.model_copy(deep=True)

        # update the notification URI in the subscription
        new_nf_events_subscription.notification_uri = build_ncof_notification_uri(
            subscription_id
        )
        
        new_nf_events_subscription.event_subscriptions[0].evt_req.rep_period = 1

        # 비동기 작업을 위한 태스크 리스트 생성
        async def execute_background_tasks():
            tasks = [
                subscribe_to_nf(
                    subscription_id=subscription_id,
                    uri=nf.get("uri") or "",
                    payload=new_nf_events_subscription.model_dump(),
                )
                for nf in nfs
            ]
            # 모든 태스크를 병렬로 실행하고 결과를 기다림
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    raise Exception("fail to subscribe")
            return True
        # 모든 NF로 subscription 이 성공해야 구독완료
        try:
            await execute_background_tasks()
            subscription_manager.add_subscription(
                subscription_id=subscription_id,
                subscription=subscription,
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error in background tasks: {str(e)}"
            )

        # subscription_manager.add_subscription(
        #     subscription_id=subscription_id,
        #     subscription=subscription,
        # )

        # for nf in nfs:
        #     background_tasks.add_task(
        #         subscribe_to_nf,
        #         subscription_id=subscription_id,
        #         uri=nf.get("uri") or "",
        #         payload=new_nf_events_subscription.model_dump(),
        #     )
        return subscription_id

    except Exception as e:
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
