import asyncio
import logging

import httpx

from openapi_server.models.event_notification import EventNotification
from openapi_server.models.nf_load_level_information import NfLoadLevelInformation
from utils.color import yellow


async def send_notification(uri: str, notification_payload: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, json=notification_payload)
            logging.info(f"{yellow('Send notification')}")
            response.raise_for_status()  # 필요하다면 HTTP 오류 발생시키기
    except httpx.RequestError as e:
        logging.error(f"Error sending background notification to {uri}: {e}")
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while sending background notification to {uri}: {e}"
        )


async def notify_multiple_times(
    uri: str, payload: dict, times: int = 3, delay: int = 2
):
    for _ in range(times):
        await asyncio.sleep(delay)
        await send_notification(uri, payload)


def create_notification_payload(nf_instance_id: str, nf_type: str) -> dict:
    """테스트용 알림 페이로드 생성"""
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
    noti = EventNotification()
    noti.nf_load_level_infos = [load_level_info]

    return noti.model_dump()
