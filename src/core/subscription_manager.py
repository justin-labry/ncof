import logging
import threading
from typing import Optional

from openapi_server.models.nncof_events_subscription import NncofEventsSubscription

from .ifc import SubscriberManagerIfc
from .subscription_handler import HandlerConfig, SubscriptionHandler

logger = logging.getLogger(__name__)

from utils.color import red, green, orange, blue, yellow, magenta, cyan, white


class SubscriptionManager(SubscriberManagerIfc):
    """
    구독 관리자 클래스

    이벤트 구독을 관리하고 각 구독에 대한 핸들러를 생성, 시작, 중지하는 역할을 담당한다.
    스레드 안전성을 보장하며, 여러 구독을 동시에 관리할 수 있다.

    Attributes:
        subscriptions (Dict[str, NncofEventsSubscription]): 구독 ID를 키로 하는 구독 정보 딕셔너리
        handlers (Dict[str, SubscriptionHandler]): 구독 ID를 키로 하는 핸들러 딕셔너리
        lock (threading.Lock): 스레드 안전성을 위한 락 객체
    """

    def __init__(self):
        self.subscriptions = {}
        self.handlers = {}
        self.lock = threading.Lock()

    def add_subscription(
        self, subscription_id: str, subscription: NncofEventsSubscription
    ) -> str:
        """
        새로운 구독을 추가하고 핸들러를 시작한다.

        기존에 동일한 구독 ID가 존재하는 경우, 기존 핸들러를 중지하고
        새로운 구독으로 교체한다.

        Args:
            subscription_id (str): 고유한 구독 식별자
            subscription (NncofEventsSubscription): 구독 정보 객체

        Returns:
            str: 성공적으로 추가된 구독의 ID

        Raises:
            ValueError: 구독 설정이 유효하지 않은 경우
            RuntimeError: 구독 핸들러 시작에 실패한 경우

        Example:
            >>> manager = SubscriptionManager()
            >>> subscription_id = manager.add_subscription("sub_001", subscription_obj)
        """

        logger.info(
            f"{green('Create subscription')} - subscription_id: '{subscription_id}'"
        )

        with self.lock:
            # 기존 구독이 있는 경우 핸들러를 중지하고 제거
            if subscription_id in self.subscriptions:
                logger.warning(
                    f"Subscription already exists - subscription_id: '{subscription_id}'"
                )
                existing_handler = self.handlers.pop(subscription_id, None)
                if existing_handler:
                    existing_handler.stop()
            try:
                config = HandlerConfig.from_ncof_events_subscription(subscription)
            except Exception as e:
                logger.error(
                    f"Failed to create HandlerConfig - subscription_id: '{subscription_id}': {e}"
                )
                raise ValueError(f"Invalid subscription configuration: {e}") from e

            # 구독 정보로부터 핸들러 설정 생성
            subscription_handler = SubscriptionHandler(
                subscription_id=subscription_id,
                handler_manager=self,
                config=config,
            )

            # 구독 정보와 핸들러를 저장
            self.subscriptions[subscription_id] = subscription
            self.handlers[subscription_id] = subscription_handler

            try:
                subscription_handler.start()  # 핸들러 시작
                logger.info(
                    f"{green('SubscriptionHandler started')} - subscription_id: '{subscription_id}'"
                )
            except Exception as e:
                # 핸들러 시작 실패 시 롤백 및 로깅
                self.subscriptions.pop(subscription_id)
                self.handlers.pop(subscription_id)
                logger.error(
                    f"Failed to start SubscriptionHandler - subscription_id: '{subscription_id}': {e}"
                )
                raise RuntimeError(f"Could not start subscription handler: {e}") from e

            return subscription_id

    def remove_subscription(self, subscription_id: str) -> bool:
        """
        지정된 구독을 제거하고 관련 핸들러를 중지한다.

        구독이 존재하지 않는 경우에도 안전하게 처리된다.

        Args:
            subscription_id (str): 제거할 구독의 식별자

        Returns:
            bool: 구독이 성공적으로 제거되었으면 True, 존재하지 않았으면 False

        Example:
            >>> manager = SubscriptionManager()
            >>> success = manager.remove_subscription("sub_001")
            >>> if success:
            ...     print("구독이 성공적으로 제거되었습니다.")
        """

        logger.info(
            f"{red("Remove subscription")} - subscription_id: '{subscription_id}'"
        )

        with self.lock:
            subscription_existed = False

            if subscription_id in self.subscriptions:
                self.subscriptions.pop(subscription_id)
                subscription_existed = True
            if subscription_id in self.handlers:
                handler = self.handlers.pop(subscription_id)
                handler.stop()
                subscription_existed = True

            return subscription_existed

    def get_subscriptions(self):
        """
        현재 활성화된 모든 구독 정보를 반환한다.

        반환되는 딕셔너리는 원본의 복사본이므로 수정해도
        원본 데이터에 영향을 주지 않습니다.

        Returns:
            Dict[str, NncofEventsSubscription]: 구독 ID를 키로 하는 구독 정보 딕셔너리

        Example:
            >>> manager = SubscriptionManager()
            >>> subscriptions = manager.get_subscriptions()
            >>> for sub_id, subscription in subscriptions.items():
            ...     print(f"구독 ID: {sub_id}")
        """
        with self.lock:
            return self.subscriptions.copy()

    def get_handler(self, subscription_id: str) -> Optional["SubscriptionHandler"]:
        """
        주어진 구독 ID로 핸들러를 찾아서 반환한다.

        """
        with self.lock:
            return self.handlers.get(subscription_id)
