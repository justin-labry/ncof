import logging

from fastapi import BackgroundTasks, Body, FastAPI, HTTPException, status

from .utils import notify_multiple_times
from openapi_server.models.event_notification import EventNotification
from openapi_server.models.nf_load_level_information import NfLoadLevelInformation
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

    noti = EventNotification()

    nf_instance_id = "ab12cd34-ef56-7890-ab12-cd34ef567891"
    nf_type = "SMF"

    load_level_info = NfLoadLevelInformation.from_dict(
        {
            "nfInstanceId": nf_instance_id,
            "snssai": {"sst": 1, "sd": "010203"},
            "nfStatus": {
                "statusRegistered": 98,
                "statusUndiscoverable": 1,
                "statusUnregistered": 1,
            },
            "nfType": nf_type,
            "nfSetId": nf_instance_id,
            "nfLoadLevelpeak": 2,
            "nfStorageUsage": 9,
            "nfCpuUsage": 2,
            "nfMemoryUsage": 123,
            "confidence": 95,
            "nfLoadLevelAverage": 3,
            "nfLoadAvgInAoi": 4,
        }
    )
    noti.nf_load_level_infos = [load_level_info]
    notification_payload = noti.model_dump()

    # 테스트를 위한 알림 기능
    if subscription.notification_uri:
        # 3번 알림 전송을 위해 백그라운드 작업 추가
        # for _ in range(3):
        #     await asyncio.sleep(2)  # 각 전송 전에 2초 대기
        #     background_tasks.add_task(
        #         send_notification,
        #         subscription.notification_uri,
        #         notification_payload,
        #     )
        background_tasks.add_task(
            notify_multiple_times,
            subscription.notification_uri,
            notification_payload,
        )

    return "smf-subscription-00001"


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
