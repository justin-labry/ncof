import asyncio
import logging

import httpx


async def send_notification(uri: str, notification_payload: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, json=notification_payload)
            logging.info(f"[Notification] ---> {uri} 응답: {response.status_code}")
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
