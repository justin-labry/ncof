import logging
from typing import Any, Dict, Optional

import httpx


import httpx
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass


# 응답 객체 정의
@dataclass
class ApiResponse:
    status_code: int
    body: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


async def _make_post_request(
    uri: str, payload: Dict[str, Any], request_id: str, log_context: str
) -> ApiResponse:
    """
    공통 HTTP POST 요청을 수행합니다.

    Args:
        uri: 요청 대상 URI
        payload: 요청 페이로드
        request_id: 요청 식별자 (로깅용)
        log_context: 로깅 컨텍스트 (예: 'subscription', 'notification')

    Returns:
        ApiResponse 객체 (상태 코드, 본문, 오류 메시지)
    """
    # logging.info(f"Sending {log_context} request to {uri} (ID: {request_id})")

    timeout = httpx.Timeout(connect=5.0, read=10.0, write=5.0, pool=5.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(uri, json=payload)
            response.raise_for_status()
            logging.info(
                f"{log_context.capitalize()} request to {uri} (ID: {request_id}) "
                f"succeeded with status {response.status_code}"
            )
            return ApiResponse(
                status_code=response.status_code,
                body=response.json() if response.content else None,
            )

    except httpx.TimeoutException as e:
        logging.error(
            f"Timeout error in {log_context} request to {uri} (ID: {request_id}): {e}"
        )
        return ApiResponse(status_code=0, error=str(e))
    except httpx.HTTPStatusError as e:
        logging.error(
            f"HTTP error in {log_context} request to {uri} (ID: {request_id}): "
            f"status {e.response.status_code}, detail {e}"
        )
        return ApiResponse(status_code=e.response.status_code, error=str(e))
    except httpx.RequestError as e:
        logging.error(
            f"Network error in {log_context} request to {uri} (ID: {request_id}): {e}"
        )
        return ApiResponse(status_code=0, error=str(e))
    except Exception as e:
        logging.error(
            f"Unexpected error in {log_context} request to {uri} (ID: {request_id}): {e}"
        )
        return ApiResponse(status_code=0, error=str(e))


async def subscribe_to_nf(
    subscription_id: str, uri: str, payload
) -> Optional[Dict[str, Any]]:
    """
    NF에 구독 요청을 보내는 비동기 함수입니다.

    Args:
        subscription_id: 구독 ID
        uri: 요청 대상 URI
        payload: 구독 요청 페이로드 (SubscriptionPayload 객체)

    Returns:
        성공 시 API 응답 본문 (딕셔너리), 실패 시 None
    """
    # if not isinstance(payload, SubscriptionPayload):
    #     logging.error(
    #         f"Invalid payload type for subscription {subscription_id}: {type(payload)}"
    #     )
    #     raise ValueError("Payload must be a SubscriptionPayload object")

    response = await _make_post_request(
        uri=uri,
        payload=payload,
        request_id=subscription_id,
        log_context="subscription",
    )
    return (
        response.body
        if response.status_code >= 200 and response.status_code < 300
        else None
    )


async def send_notification(
    notification_id: str, uri: str, payload: Dict[str, Any]
) -> int:
    """
    알림을 보내는 비동기 함수입니다.

    Args:
        notification_id: 알림 ID
        uri: 요청 대상 URI
        payload: 알림 페이로드 (딕셔너리)

    Returns:
        HTTP 상태 코드 (성공/실패 여부에 따라)
    """
    response = await _make_post_request(
        uri=uri, payload=payload, request_id=notification_id, log_context="notification"
    )
    return response.status_code
