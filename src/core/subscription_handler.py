import time
import threading
import queue
import asyncio
import logging

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from openapi_server.models.event_notification import EventNotification
from openapi_server.models.nf_load_level_information import NfLoadLevelInformation

from .nf_load_aggregator import calculate_average_loads
from .nf_client import send_notification
from .ifc import SubscriberManagerIfc

logger = logging.getLogger(__name__)
TIMEZONE: timezone = timezone(timedelta(hours=9))

from utils.color import red, green, orange, blue, yellow, magenta, cyan, white


@dataclass(frozen=True)  # 불변으로 설정
class HandlerConfig:
    """주기적 보고를 위한 설정을 담는 데이터 클래스"""

    rep_period: float  # 알림 처리 주기 (초)
    max_report_nbr: int  # 최대 보고 횟수
    mon_dur: Optional[datetime]  # 모니터링 지속 시간 (초, 선택)
    start_ts: Optional[datetime]  # 시작 타임스탬프 (선택)
    end_ts: Optional[datetime]  # 종료 타임스탬프 (선택)
    notif_method: str  # 알림 방법

    notification_uri: Optional[str]  # 알림 URI (선택)
    log_level: int = logging.INFO  # 로그 레벨 기본값

    # 클래스 상수: 기본값 정의
    DEFAULT_rep_period_SEC = 5.0  # 기본 보고 주기
    DEFAULT_MAX_REPORT_NBR = 0  # 기본 최대 보고 횟수, 0이면 무제한

    MAX_NOTIFICATIONS = 100
    MAX_AGE_MINUTES = 5

    def __post_init__(self):
        """설정값 유효성 검사"""
        if self.rep_period <= 0:
            raise ValueError("rep_period must be positive")
        if self.max_report_nbr < 0:
            raise ValueError("max_report_nbr cannot be negative")
        if (
            self.start_ts is not None
            and self.end_ts is not None
            and self.start_ts >= self.end_ts
        ):
            raise ValueError("start_ts must be earlier than end_ts")

    @staticmethod
    def from_ncof_events_subscription(ncof_events_subscription) -> "HandlerConfig":
        """
        ncof_events_subscription에서 설정값을 추출해 HandlerConfig를 생성한다.

        Args:
            ncof_events_subscription: 이벤트 구독 객체
        Returns:
            HandlerConfig: 추출된 설정값으로 채워진 설정 객체
        """
        event_subscription = ncof_events_subscription.event_subscriptions[0]
        evt_req = getattr(event_subscription, "evt_req", None)
        extra_report_req = getattr(event_subscription, "extra_report_req", None)

        rep_period = getattr(
            evt_req, "rep_period", HandlerConfig.DEFAULT_rep_period_SEC
        )
        max_report_nbr = getattr(
            evt_req, "max_report_nbr", HandlerConfig.DEFAULT_MAX_REPORT_NBR
        )

        mon_dur = getattr(evt_req, "mon_dur", None)
        start_ts = getattr(extra_report_req, "start_ts", None)
        end_ts = getattr(extra_report_req, "end_ts", None)

        notif_method = getattr(evt_req, "notif_method", "PERIODIC")

        notification_uri = getattr(ncof_events_subscription, "notification_uri", None)

        return HandlerConfig(
            rep_period=rep_period,
            max_report_nbr=max_report_nbr,
            mon_dur=mon_dur,
            start_ts=start_ts,
            end_ts=end_ts,
            notif_method=notif_method,
            notification_uri=notification_uri,
            log_level=logging.INFO,
        )


@dataclass
class TimedNotification:
    """타임스탬프를 포함하는 알림 데이터 클래스"""

    timestamp: float
    notification: NfLoadLevelInformation


class SubscriptionHandler(threading.Thread):
    """구독 요청을 처리하고 조건에 따라 알림을 전송하는 스레드 클래스"""

    def __init__(
        self,
        subscription_id: str,
        handler_manager: SubscriberManagerIfc,
        config: HandlerConfig,
    ):
        super().__init__(daemon=True)

        self.subscription_id = subscription_id
        self.subscription_manager = handler_manager
        self.notifications: list[TimedNotification] = []
        self.start_time = time.time()
        self.loop = asyncio.get_event_loop()
        self.lock = threading.Lock()
        self.config = config

        self.report_count = 0
        self.running = True

    def _has_reached_limit(self):
        current_time = datetime.now(TIMEZONE)
        elapsed_time = time.time() - self.start_time
        logger.debug(
            f"Checking limits: subscription_id={self.subscription_id}"
            f"elapsed_time={elapsed_time:.2f}s"
            f"report_count={self.report_count}"
        )

        if self.config.end_ts and current_time >= self.config.end_ts:
            logger.info(f"{red('종료조건')} - end_ts exceeded ({self.config.end_ts})")
            return True

        if self.config.mon_dur is not None and current_time >= self.config.mon_dur:
            logging.info(
                f"{red('종료조건')} - mon_dur exceeded ({self.config.mon_dur})"
            )
            return True

        if self.report_count >= self.config.max_report_nbr:
            logging.info(
                f"{red('종료조건')} - max_report_nbr excedeed ({self.config.max_report_nbr})"
            )
            return True

        return False

    def _get_nf_loads(
        self, create_default_if_empty: bool = False
    ) -> Dict[str, list[NfLoadLevelInformation]]:
        """
        저장된 알림 목록에서 최근 5분 내의 데이터를 필터링하고, nf_instance_id별로 그룹화한다.
        처리할 데이터가 없는 경우 기본값을 포함하는 통계 정보를 생성합니다.
        """
        with self.lock:
            # 처리할 알림을 복사합니다.
            notifications_to_process = self.notifications[:]
            # 이벤트 기반 알림(PERIODIC이 아닌 경우)은 처리 후 목록을 비워 중복 전송방지
            if self.config.notif_method != "PERIODIC":
                self.notifications.clear()

        five_minutes_ago = time.time() - (self.config.MAX_AGE_MINUTES * 60)

        recent_notifications = [
            item.notification
            for item in notifications_to_process
            if item.timestamp >= five_minutes_ago
        ]

        nf_loads: Dict[str, list[NfLoadLevelInformation]] = {}
        for nf_load_level_info in recent_notifications:
            nf_instance_id = nf_load_level_info.nf_instance_id
            if not nf_instance_id:
                continue
            if nf_instance_id not in nf_loads:
                nf_loads[nf_instance_id] = []
            nf_loads[nf_instance_id].append(nf_load_level_info)

        return nf_loads

    def _send_callback_to_nf(
        self, nf_load_level_infos_by_nf: Dict[str, list[NfLoadLevelInformation]]
    ):
        """통계정보 콜백처리"""

        if not self.config.notification_uri:
            logger.info("notification_uri missed")
            return

        nf_load_level_infos = calculate_average_loads(nf_load_level_infos_by_nf)

        if not nf_load_level_infos:
            return

        event_notification = EventNotification()
        event_notification.nf_load_level_infos = nf_load_level_infos

        try:
            # 클라이언트 콜백 URL로 알림 전송
            status_code = asyncio.run_coroutine_threadsafe(
                send_notification(
                    notification_id=self.subscription_id,
                    uri=self.config.notification_uri,
                    payload=event_notification.model_dump(),
                ),
                self.loop,
            ).result()
            if 200 <= status_code < 300:
                logger.debug(f"Notification sent successfully: {self.subscription_id}")
            else:
                logger.warning(
                    f"Notification sending failed: {self.subscription_id},"
                    f"Status code={status_code}"
                )
        except asyncio.TimeoutError:
            logger.error(f"Notification timeout: {self.subscription_id}")
        except ConnectionError:
            logger.error(f"Connection failed: {self.subscription_id}")
        except Exception as e:
            logger.error(f"Unexpected error: {self.subscription_id} {e}", exc_info=True)

    def _check_value_change(self, nf_load_info) -> bool:
        return True

    def _check_threshold_exceeded(self, nf_load_info) -> bool:
        return True

    def _process_queued_notifications(
        self, create_default_if_empty: bool = False
    ) -> bool:
        """
        notification_queue에서 모든 알림을 가져와 처리하고 전송한다.
        알림이 성공적으로 전송되었으면 True를 반환한다.
        """
        nf_loads = self._get_nf_loads(create_default_if_empty=create_default_if_empty)
        if not nf_loads:
            return False

        self._send_callback_to_nf(nf_loads)
        self._increase_report_count()
        return True

    def _process_on_event_detection(self):
        """ON_EVENT_DETECTION: 이벤트 감지 즉시 처리"""
        if self._process_queued_notifications(create_default_if_empty=False):
            logger.info(
                f"[{self.subscription_id}] 🚨 ON_EVENT_DETECTION Notify ---> NF"
            )

    def _process_on_change(self):
        pass

    def _process_on_threshold(self):
        pass

    def _increase_report_count(self):
        self.report_count += 1

    def run(self):
        logger.info(f"Start handler: {self.subscription_id}")
        last_report_time = time.time()
        notif_method = self.config.notif_method

        while self.running:
            # 구독 만료 또는 핸들러 중지 조건 확인
            if self._has_reached_limit():
                self.running = False
                break

            current_time = datetime.now(TIMEZONE)
            if self.config.start_ts and current_time < self.config.start_ts:
                logger.debug(
                    f"[{self.subscription_id}] Waiting for start_ts: {self.config.start_ts}"
                )
                time.sleep(1)
                continue

            try:
                # notif_method에 따른 처리
                if notif_method == "PERIODIC":
                    if time.time() - last_report_time >= self.config.rep_period:
                        if self._process_queued_notifications():
                            logger.info(
                                f"[{self.subscription_id}] {green('PERIODIC Notify')} ---> NF"
                            )
                        last_report_time = time.time()
                # 이벤트 기반 처리 (ON_EVENT_DETECTION, ON_CHANGE 등)
                elif self.notifications:  # 리스트가 비어있지 않을 때만 처리
                    if notif_method == "ON_EVENT_DETECTION":
                        self._process_on_event_detection()
                    elif notif_method == "ON_CHANGE":
                        self._process_on_change()
                    elif notif_method == "ON_THRESHOLD":
                        self._process_on_threshold()

                # CPU 사용을 줄이기 위해 짧은 대기 시간 추가
                time.sleep(1)

            except Exception as e:
                logger.error(f"Error during notification processing: {str(e)}")
                time.sleep(1.0)  # 오류 발생 시 잠시 대기

        # 핸들러 종료 및 리소스 정리
        logger.debug(
            f"[Subscription Expired]: {self.subscription_id} "
            f"Elapsed Time: {(time.time() - self.start_time):.2f} seconds, "
            f"Notification Count: {self.report_count}"
        )
        self.subscription_manager.remove_subscription(self.subscription_id)

    def add_load_info(self, notification: NfLoadLevelInformation):
        if not self.running:
            return

        with self.lock:
            # Wrapper 클래스를 사용하여 타임스탬프와 함께 저장
            timed_notification = TimedNotification(
                timestamp=time.time(), notification=notification
            )
            self.notifications.append(timed_notification)

            # 리스트 크기를 100개로 유지
            if len(self.notifications) > self.config.MAX_NOTIFICATIONS:
                self.notifications.pop(0)

            logger.info(
                f"Add loads: {self.subscription_id}"
                f"List size: {len(self.notifications)}",
            )

    def stop(self):
        """핸들러 중지"""
        self.running = False
        logger.info(f"{red('Handler stopped')}: {self.subscription_id}")
