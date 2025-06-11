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

        config = HandlerConfig.from_ncof_events_subscription(subscription)
        # 구독 핸들러 생성
        subscription_handler = SubscriptionHandler(
            subscription_id=subscription_id,
            handler_manager=self,
            config=config,
        )

        self.subscriptions[subscription_id] = subscription
        self.handlers[subscription_id] = subscription_handler

        subscription_handler.start()

        return subscription_id

    def remove_subscription(self, subscription_id: str) -> bool:
        """구독 제거"""
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
        with self.lock:
            return self.subscriptions

    def get_handler(self, subscription_id: str) -> Optional["SubscriptionHandler"]:
        """구독 ID로 핸들러 찾기"""
        return self.handlers.get(subscription_id)
