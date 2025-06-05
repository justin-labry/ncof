# coding: utf-8

from fastapi.testclient import TestClient


from typing import Any  # noqa: F401
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription  # noqa: F401
from openapi_server.models.problem_details import ProblemDetails  # noqa: F401


def test_create_ncof_events_subscription(client: TestClient):
    """Test case for create_ncof_events_subscription

    Create a new Individual NCOF Events Subscription
    """
    nncof_events_subscription = {

        "eventSubscriptions": [
            {
                "anySlice": True,
                "appIds": [
                    "nfload-mobility-watcher-v1"
                ],
                "event": "NF_LOAD",
                "extraReportReq": {
                    "startTs": "2025-05-27T07:16:00.000+09:00",
                    "endTs": "2025-05-30T17:16:00.000+09:00"
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
                    "aggTrafficRate": "80.0 Gbps"
                }
                ],
                "nfInstanceIds": [
                    "3fa85f64-amf-4562-b3fc-2c963f66afa6"
                ],
                "nfTypes": [
                    "AMF", "SMF"
                ],
                "evtReq": {
                    "immRep": False,
                    "notifMethod": "PERIODIC",
                    "maxReportNbr": 50,
                    "mon_dur": "2025-05-30T17:30:00.000+09:00",
                    "repPeriod": 5,
                    "sampRatio": 75,
                    "partitionCriteria": [
                        "TAC"
                    ],
                    "grpRepTime": 0,
                    "notifFlag": "ACTIVATE",
                    "notifFlagInstruct": {
                        "bufferedNotifs": "SEND_ALL",
                        "subscription": "CLOSE"
                    },
                    "mutingSetting": {
                        "maxNoOfNotif": 0,
                        "durationBufferedNotif": 0
                    }
                }
            }
        ],
        "notification_uri": "http://localhost:8081/callbacks/notifications",
        "notifCorrId": "string",
        "supportedFeatures": "040",
        "prevSub": "string",
        "consNfInfo": "string"

    }

    headers = {
        "Authorization": "Bearer special-key",
    }

    response = client.request(
        "POST",
        "/subscriptions",
        headers=headers,
        json=nncof_events_subscription,
    )

    assert response.status_code == 201
