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

from .load_aggregator import aggregate
from .nf_client import send_notification
from .ifc import SubscriberManagerIfc

logger = logging.getLogger(__name__)
TIMEZONE: timezone = timezone(timedelta(hours=9))


@dataclass(frozen=True)  # 불변으로 설정
class HandlerConfig:
    """주기적 보고를 위한 설정을 담는 데이터 클래스"""

    report_period: float  # 알림 처리 주기 (초)
    max_report_nbr: int  # 최대 보고 횟수
    mon_dur: Optional[datetime]  # 모니터링 지속 시간 (초, 선택)
    start_ts: Optional[datetime]  # 시작 타임스탬프 (선택)
    end_ts: Optional[datetime]  # 종료 타임스탬프 (선택)
    notification_uri: Optional[str]  # 알림 URI (선택)
    log_level: int = logging.INFO  # 로그 레벨 기본값

    # 클래스 상수: 기본값 정의
    DEFAULT_REPORT_PERIOD_SEC = 5.0  # 기본 보고 주기
    DEFAULT_MAX_REPORT_NBR = 0  # 기본 최대 보고 횟수, 0이면 무제한

    def __post_init__(self):
        """설정값 유효성 검사"""
        if self.report_period <= 0:
            raise ValueError("report_period must be positive")
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
        ncof_events_subscription에서 설정값을 추출해 HandlerConfig를 생성.

        Args:
            ncof_events_subscription: 이벤트 구독 객체
        Returns:
            HandlerConfig: 추출된 설정값으로 채워진 설정 객체
        """
        event_subscription = ncof_events_subscription.event_subscriptions[0]
        evt_req = getattr(event_subscription, "evt_req", None)
        extra_report_req = getattr(event_subscription, "extra_report_req", None)

        report_period = getattr(
            evt_req, "rep_period", HandlerConfig.DEFAULT_REPORT_PERIOD_SEC
        )
        max_report_nbr = getattr(
            evt_req, "max_report_nbr", HandlerConfig.DEFAULT_MAX_REPORT_NBR
        )
        mon_dur = getattr(evt_req, "mon_dur", None)
        start_ts = getattr(extra_report_req, "start_ts", None)
        end_ts = getattr(extra_report_req, "end_ts", None)
        notification_uri = getattr(ncof_events_subscription, "notification_uri", None)

        return HandlerConfig(
            report_period=report_period,
            max_report_nbr=max_report_nbr,
            mon_dur=mon_dur,
            start_ts=start_ts,
            end_ts=end_ts,
            notification_uri=notification_uri,
            log_level=logging.INFO,
        )


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
        self.notification_queue = queue.Queue()
        self.start_time = time.time()
        self.loop = asyncio.get_event_loop()  # 기존 이벤트 루프 재사용
        self.lock = threading.Lock()
        self.config = config

        self.report_count = 0
        self.running = True

    def _has_reached_limit(self):
        current_time = datetime.now(TIMEZONE)
        elapsed_time = time.time() - self.start_time
        logger.debug(
            f"Checking limits: subscription_id={self.subscription_id}, elapsed_time={elapsed_time:.2f}s, report_count={self.report_count}"
        )

        if self.config.start_ts and current_time < self.config.start_ts:
            logger.debug(f"🛑 [start_ts] not yet started ({self.config.start_ts})")
            return False

        if self.config.end_ts and current_time >= self.config.end_ts:
            logger.info(f"🛑 [end_ts] exceeded ({self.config.end_ts})")
            return True

        if self.config.mon_dur is not None and current_time >= self.config.mon_dur:
            logging.info(f"🛑 [mon_dur] exceeded ({self.config.mon_dur})")
            return True

        if self.report_count >= self.config.max_report_nbr:
            logging.info(f"🛑 [max_report_nbr] excedeed ({self.config.max_report_nbr})")
            return True

        return False

    def _aggregate_loads(
        self, nf_loads: Dict[str, list[NfLoadLevelInformation]]
    ) -> None:
        """
        notification_queue에서 모든 알림을 가져와 nf_load_infos에 nf_instance_id별로 저장.

        Args:
            nf_load_infos: nf_instance_id를 키로, NfLoadLevelInformation 리스트를 값으로 가지는 딕셔너리
        """
        while not self.notification_queue.empty():
            nf_load_level_info = self.notification_queue.get_nowait()
            nf_instance_id = nf_load_level_info.nf_instance_id

            # nf_instance_id 별로 로드 정보 저장
            if nf_instance_id not in nf_loads:
                nf_loads[nf_instance_id] = []
            nf_loads[nf_instance_id].append(nf_load_level_info)
            self.notification_queue.task_done()

    def _process_notifications(
        self, notifications: Dict[str, list[NfLoadLevelInformation]]
    ):
        """알림 데이터 처리 및 클라이언트에 통지"""

        if not self.config.notification_uri:
            logger.info("notification_uri missed")
            return

        nf_load_level_infos = aggregate(notifications)

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

        except Exception as e:
            logger.error(
                f"Error during notification sending: {self.subscription_id}, Error={str(e)}"
            )

    def run(self):
        logger.info(f"Start handler: {self.subscription_id}")
        nf_load_infos: Dict[str, list[NfLoadLevelInformation]] = {}
        last_time = time.time()
        while True:
            current_time = time.time()
            with self.lock:
                if not self.running or self._has_reached_limit():
                    logger.debug(
                        f"[Subscription Expired]: {self.subscription_id} "
                        f"Elapsed Time: {(time.time() - self.start_time):.2f} seconds, "
                        f"Notification Count: {self.report_count}"
                    )
                    self.running = False
                    self.subscription_manager.remove_subscription(self.subscription_id)
                    break

                try:
                    if current_time - last_time >= self.config.report_period:
                        self._aggregate_loads(nf_load_infos)
                        self._process_notifications(nf_load_infos)
                        logger.info(f"[{self.subscription_id}] Notify ---> NF")
                        self.report_count += 1
                        # nf_load_infos.clear()
                        last_time = time.time()
                    elapsed_time = time.time() - last_time
                    sleep_time = max(0, self.config.report_period - elapsed_time)
                    time.sleep(sleep_time)
                except Exception as e:
                    logger.error(f"Error during notification processing: {str(e)}")
                    elapsed_time = time.time() - last_time
                    sleep_time = max(0, self.config.report_period - elapsed_time)
                    time.sleep(sleep_time)

    def add_notification(self, notification: NfLoadLevelInformation):
        if self.running:
            self.notification_queue.put(notification)
            logger.info(
                f"Add notification: {self.subscription_id}, Queue size: {self.notification_queue.qsize()}"
            )

    def stop(self):
        """핸들러 중지"""
        self.running = False
        logger.info(f"Stop handler: {self.subscription_id}")
