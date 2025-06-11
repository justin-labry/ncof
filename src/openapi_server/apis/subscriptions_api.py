# coding: utf-8

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

router = APIRouter()

from ..config.app_config import app_config


def get_ncof_notification_uri(subscription_id: str) -> str:
    # return f"http://{SERVER_IP}:{PORT}/callbacks/notifications/{subscription_id}"
    return f"http://localhost:8080/{app_config.notification_prefix}/{subscription_id}"


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
        # success = dispatcher.subscribe(subscription_id, ncof_events_subscription)

        new_nf_events_subscription = subscription.model_copy()

        # 구독 ID를 생성한다.
        # subscription_id = "subscription-0001"
        subscription_id = str(uuid.uuid4())
        # update the notification URI in the subscription
        new_nf_events_subscription.notification_uri = get_ncof_notification_uri(
            subscription_id
        )

        subscription_manager.add_subscription(
            subscription_id=subscription_id,
            subscription=subscription,
        )

        for nf in nfs:
            background_tasks.add_task(
                subscribe_to_nf,
                subscription_id=subscription_id,
                uri=nf.get("uri") or "",
                payload=new_nf_events_subscription.model_dump(),
            )

        return subscription_id

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subscribing: {str(e)}")
    # return await subscription_service.create_ncof_events_subscription(subscription)


@router.get("/subscriptions")
async def subscriptions(
    subscription_manager: SubscriptionManager = Depends(get_subscription_manager),
):
    return subscription_manager.get_subscriptions()
