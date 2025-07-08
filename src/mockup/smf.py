import logging

from fastapi import BackgroundTasks, Body, FastAPI, HTTPException, status

from .utils import create_notification_payload, notify_multiple_times
from openapi_server.models.event_notification import EventNotification
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription


app = FastAPI(title="SMF Simulator")

@app.post("/subscriptions")
async def subscribe(
    background_tasks: BackgroundTasks,  # BackgroundTasks 주입
    subscription: NncofEventsSubscription = Body(None, description=""),
):
    if not subscription or not subscription.notification_uri:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body is missing or notification_uri is not provided.",
        )
    logging.info(f"[Subscription] <--- {subscription.notification_uri}")

    nf_instance_id = "ab12cd34-ef56-7890-ab12-cd34ef567891"
    nf_type = "SMF"

    # 설정 값과 헬퍼 함수를 사용하여 페이로드 생성
    notification_payload = create_notification_payload(
        nf_instance_id=nf_instance_id,
        nf_type=nf_type,
    )

    # 테스트를 위한 알림 기능
    if subscription.notification_uri:
        background_tasks.add_task(
            notify_multiple_times,
            subscription.notification_uri,
            notification_payload,
        )

    subscription_id = "smf-subscription-00001"
    logging.info(f"Background notification task added for {subscription.notification_uri}")

    return subscription_id


print(
    r"""
 ____  __  __ _____   __  __            _
/ ___||  \/  |  ___| |  \/  | ___   ___| | ___   _ _ __
\___ \| |\/| | |_    | |\/| |/ _ \ / __| |/ / | | | '_ \
 ___) | |  | |  _|   | |  | | (_) | (__|   <| |_| | |_) |
|____/|_|  |_|_|     |_|  |_|\___/ \___|_|\_\\__,_| .__/
                                                  |_|
    """
)
