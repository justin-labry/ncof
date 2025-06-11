from dataclasses import dataclass
import logging
import yaml


@dataclass
class AppConfig:
    host: str = "0.0.0.0"
    port: int = 8080
    server_ip: str = "localhost"
    simulator: bool = False
    report_period: int = 5
    notification_prefix: str = ""
    subscription_prefix: str = ""


def _load_config(file_path: str) -> AppConfig:
    """
    YAML 설정 파일을 로드하여 AppConfig 객체로 반환합니다.
    설정 파일이 없거나 파싱에 실패하면 기본 설정을 반환합니다.

    Args:
        file_path: 설정 파일 경로
    Returns:
        AppConfig 객체
    """
    default_config = AppConfig()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        if not isinstance(config, dict):
            logging.error(f"설정 파일 '{file_path}'가 올바른 딕셔너리 형식이 아닙니다.")
            return default_config

        # ncof_server 하위 설정 가져오기
        ncof_config = config.get("ncof_server", {})

        # 설정값 업데이트
        return AppConfig(
            host=config.get("host", default_config.host),
            port=config.get("port", default_config.port),
            server_ip=ncof_config.get("server_ip", default_config.server_ip),
            simulator=ncof_config.get("simulator", default_config.simulator),
            report_period=ncof_config.get(
                "report_period", default_config.report_period
            ),
            notification_prefix=ncof_config.get(
                "notification_prefix", default_config.notification_prefix
            ),
            subscription_prefix=ncof_config.get(
                "subscription_prefix", default_config.subscription_prefix
            ),
        )
    except FileNotFoundError:
        logging.error(
            f"설정 파일 '{file_path}'를 찾을 수 없습니다. 기본 설정을 사용합니다."
        )
        return default_config
    except yaml.YAMLError as exc:
        logging.error(f"YAML 파일 파싱 중 오류 발생: {exc}. 기본 설정을 사용합니다.")
        return default_config


CONFIG_FILE_PATH = "ncof_server.yaml"

# 설정 로드
app_config: AppConfig = _load_config(CONFIG_FILE_PATH)
