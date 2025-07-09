import logging
import json
import httpx
import asyncio
import threading
import uvicorn
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, Body, FastAPI, HTTPException, status
from .utils import create_notification_payload, notify_multiple_times
from openapi_server.models.event_notification import EventNotification
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription

async def subscribe():
    """
    Subscribes to the NCOF service.
    """
    logging.info("Subscribing to NCOF...")
    await send_subscription(ncof_url, event_subscription.model_dump())
    logging.info("Subscription request sent.")


app = FastAPI(title="NF Mockup")


@app.post("/callbacks/notifications")
async def receive_notification(
    background_tasks: BackgroundTasks,  # BackgroundTasks 주입
    event_notification: EventNotification = Body(None, description=""),
):

    print(json.dumps(event_notification.model_dump(), indent=2))

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


event_subscription = NncofEventsSubscription.from_dict(
    {
        "eventSubscriptions": [
            {
                "anySlice": True,
                "appIds": ["nfload-mobility-watcher-v1"],
                "event": "NF_LOAD",
                "extraReportReq": {
                    "startTs": "2025-06-09T07:16:00.000+09:00",
                    "endTs": "2025-07-09T18:00:00.000+09:00",
                },
                "notificationMethod": "PERIODIC",
                "nfLoadLvlThds": [
                    {
                        "nfLoadLevel": 70,
                        "nfCpuUsage": 80,
                        "nfMemoryUsage": 80,
                        "nfStorageUsage": 80,
                        "avgTrafficRate": "20 Gbps",
                        "maxTrafficRate": "40 Gbps",
                        "aggTrafficRate": "80.0 Gbps",
                    }
                ],
                "nfInstanceIds": ["3fa85f64-amf-4562-b3fc-2c963f66afa6"],
                "nfTypes": ["SMF"],
                "evtReq": {
                    "immRep": False,
                    "notifMethod": "PERIODIC",
                    "maxReportNbr": 2,
                    "monDur": "2025-07-09T18:00:00.000+09:00",
                    "repPeriod": 1,
                    "sampRatio": 75,
                    "partitionCriteria": ["TAC"],
                    "grpRepTime": 0,
                    "notifFlag": "ACTIVATE",
                    "notifFlagInstruct": {
                        "bufferedNotifs": "SEND_ALL",
                        "subscription": "CLOSE",
                    },
                    "mutingSetting": {"maxNoOfNotif": 0, "durationBufferedNotif": 0},
                },
            }
        ],
        "notificationURI": "http://localhost:8081/callbacks/notifications",
        "notifCorrId": "string",
        "supportedFeatures": "040",
        "prevSub": "string",
        "consNfInfo": "string",
    }
)

ncof_url = "http://localhost:8080/ETRI_INRS_TEAM/NCOF_Nncof_EventSubscription/1.0.0/subscriptions"

# print(event_subscription)


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8081)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    while True:
        command = input("Enter 'subscribe' to send subscription, or 'exit' to quit: ")
        if command.lower() == "subscribe":
            asyncio.run(subscribe())
        elif command.lower() == "exit":
            break
        else:
            print("Unknown command.")