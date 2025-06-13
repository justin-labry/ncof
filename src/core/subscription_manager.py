from typing import Optional
import threading
import logging

from openapi_server.models.nncof_events_subscription import NncofEventsSubscription

from .ifc import SubscriberManagerIfc
from .subscription_handler import HandlerConfig, SubscriptionHandler

logger = logging.getLogger(__name__)


class SubscriptionManager(SubscriberManagerIfc):
    """구독 관리자 클래스"""

    def __init__(self):
        self.subscriptions = {}
        self.handlers = {}
        self.lock = threading.Lock()

    def add_subscription(
        self, subscription_id: str, subscription: NncofEventsSubscription
    ) -> str:
        """새로운 구독을 추가하고 핸들러를 시작한다."""
        with self.lock:
            if subscription_id in self.subscriptions:
                logger.warning(
                    f"Subscription ID '{subscription_id}' already exists. Updating subscription."
                )
                # 기존 핸들러를 중지하고 제거하는 로직 추가 가능
                existing_handler = self.handlers.pop(subscription_id, None)
                if existing_handler:
                    existing_handler.stop()
            try:
                config = HandlerConfig.from_ncof_events_subscription(subscription)
            except Exception as e:
                logger.error(
                    f"Failed to create HandlerConfig for subscription '{subscription_id}': {e}"
                )
                raise ValueError(f"Invalid subscription configuration: {e}") from e

            # 구독 핸들러 생성
            subscription_handler = SubscriptionHandler(
                subscription_id=subscription_id,
                handler_manager=self,
                config=config,
            )

            self.subscriptions[subscription_id] = subscription
            self.handlers[subscription_id] = subscription_handler

            try:
                subscription_handler.start()  # 핸들러 시작
                logger.info(
                    f"Subscription '{subscription_id}' added and handler started."
                )
            except Exception as e:
                # 핸들러 시작 실패 시 롤백 및 로깅
                self.subscriptions.pop(subscription_id)
                self.handlers.pop(subscription_id)
                logger.error(
                    f"Failed to start handler for subscription '{subscription_id}': {e}"
                )
                raise RuntimeError(f"Could not start subscription handler: {e}") from e

            return subscription_id

    def remove_subscription(self, subscription_id: str) -> bool:
        """구독을 제거하고 관련 핸들러를 중지한다."""
        with self.lock:

            if subscription_id in self.subscriptions:
                self.subscriptions.pop(subscription_id)
            if subscription_id in self.handlers:
                handler = self.handlers.pop(subscription_id)
                handler.stop()
                logger.info(f"Remove subscription: {subscription_id}")
                return True
        return False

    def get_subscriptions(self):
        """현재 활성화된 모든 구독 정보를 반환한다."""
        with self.lock:
            return self.subscriptions.copy()

    def get_handler(self, subscription_id: str) -> Optional["SubscriptionHandler"]:
        """주어진 구독 ID로 핸들러를 찾아서 반환한다."""
        with self.lock:
            return self.handlers.get(subscription_id)
