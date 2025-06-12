import logging

from fastapi import BackgroundTasks, Body, FastAPI

from mockup.utils import notify_multiple_times
from openapi_server.models.event_notification import EventNotification
from openapi_server.models.nf_load_level_information import NfLoadLevelInformation
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription


# FastAPI 앱 생성
app = FastAPI(title="AMF Simulator")

@app.post("/subscriptions")
async def subscribe(
    background_tasks: BackgroundTasks,  # BackgroundTasks 주입
    subscription: NncofEventsSubscription = Body(None, description=""),
):
    logging.info(f"[Subscription] <--- {subscription.notification_uri}")

    noti = EventNotification()

    nf_instance_id = "ab12cd34-ef56-7890-ab12-cd34ef567890"
    nf_type = "AMF"

    load_level_info = NfLoadLevelInformation.from_dict(
        {
            "nfInstanceId": nf_instance_id,
            "nfType": nf_type,
            "nfSetId": nf_instance_id,
            "snssai": {"sst": 1, "sd": "010203"},
            "nfStatus": {
                "statusRegistered": 98,
                "statusUndiscoverable": 1,
                "statusUnregistered": 1,
            },
            "confidence": 95,
            "nfStorageUsage": 9,
            "nfLoadLevelpeak": 2,
            "nfCpuUsage": 2,
            "nfMemoryUsage": 123,
            "nfLoadLevelAverage": 3,
            "nfLoadAvgInAoi": 4,
        }
    )
    noti.nf_load_level_infos = [load_level_info]
    notification_payload = noti.model_dump()

    # 테스트를 위한 알림 기능
    if subscription.notification_uri:
        background_tasks.add_task(
            notify_multiple_times,
            subscription.notification_uri,
            notification_payload,
        )
    return "amf-subscription-00001"


print(
    r"""
    _    __  __ _____   __  __            _
   / \  |  \/  |  ___| |  \/  | ___   ___| | ___   _ _ __
  / _ \ | |\/| | |_    | |\/| |/ _ \ / __| |/ / | | | '_ \
 / ___ \| |  | |  _|   | |  | | (_) | (__|   <| |_| | |_) |
/_/   \_\_|  |_|_|     |_|  |_|\___/ \___|_|\_\\__,_| .__/
                                                    |_|
    """
)
