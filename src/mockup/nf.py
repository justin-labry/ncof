import logging
import json
import httpx
import asyncio
import threading
import uvicorn

from fastapi import BackgroundTasks, Body, FastAPI

from openapi_server.models.event_notification import EventNotification
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription
from utils.color import red, green, orange, blue, yellow, magenta, cyan, white


async def subscribe():
    """
    Subscribes to the NCOF service.
    """
    logging.info("Subscribing to NCOF...")
    res = await send_subscription(ncof_url, event_subscription.model_dump())
    logging.info("Subscription request sent.")
    logging.info(res.content.decode("utf-8"))


app = FastAPI(title="NF Mockup")


@app.post("/callbacks/notifications")
async def receive_notification(
    background_tasks: BackgroundTasks,  # BackgroundTasks 주입
    event_notification: EventNotification = Body(None, description=""),
):
    if event_notification.nf_load_level_infos is not None:
        load_level_info = event_notification.nf_load_level_infos[0]
    else:
        return

    nf_instance_id = load_level_info.nf_instance_id
    nf_type = load_level_info.nf_type
    cpu_usage = load_level_info.nf_cpu_usage
    memory_usage = load_level_info.nf_memory_usage
    storage_usage = load_level_info.nf_storage_usage

    logging.info(f"{green('Receive notification')}")
    logging.info(f"  [{nf_type}] - {nf_instance_id}")
    logging.info(f"  CPU: {cpu_usage} Memory: {memory_usage} Storage: {storage_usage}")

    # print(json.dumps(event_notification.model_dump(), indent=2))

    return


print(
    r"""
 _   _ _____   __  __            _
| \ | |  ___| |  \/  | ___   ___| | ___   _ _ __
|  \| | |_    | |\/| |/ _ \ / __| |/ / | | | '_ \
| |\  |  _|   | |  | | (_) | (__|   <| |_| | |_) |
|_| \_|_|     |_|  |_|\___/ \___|_|\_\\__,_| .__/
                                           |_|
    """
)


async def send_subscription(uri: str, payload: dict):

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, json=payload)
            logging.info(f"[Notification] ---> {uri} 응답: {response.status_code}")
            response.raise_for_status()  # 필요하다면 HTTP 오류 발생시키기

    except httpx.RequestError as e:
        logging.error(f"Error sending background notification to {uri}: {e}")
    except Exception as e:

        logging.error(
            f"An unexpected error occurred while sending background notification to {uri}: {e}"
        )
    return response


def load_subscription_from_file(file_path: str) -> NncofEventsSubscription:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            subscription_data = json.load(f)
        return NncofEventsSubscription.from_dict(subscription_data)
    except FileNotFoundError:
        logging.error(f"Subscription file not found at {file_path}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from {file_path}")
        return None


event_subscription = load_subscription_from_file("src/mockup/subscription.json")

ncof_url = "http://localhost:8080/ETRI_INRS_TEAM/NCOF_Nncof_EventSubscription/1.0.0/subscriptions"


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8081, log_config="log_config.ini")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    while True:
        command = input("Enter 's' to send subscription, or 'q' to quit: ")
        if command.lower() == "s":
            asyncio.run(subscribe())
        elif command.lower() == "q":
            break
        else:
            logging.info("Unknown command.")
