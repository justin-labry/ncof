# coding: utf-8

from fastapi.testclient import TestClient

from pydantic import Field, StrictStr  # noqa: F401
from typing import Any  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.nncof_events_subscription import NncofEventsSubscription  # noqa: F401
from openapi_server.models.problem_details import ProblemDetails  # noqa: F401
from openapi_server.models.redirect_response import RedirectResponse  # noqa: F401

def test_delete_ncof_events_subscription(client: TestClient):
    """Test case for delete_ncof_events_subscription

    Delete an existing Individual NCOF Events Subscription
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    response = client.request(
        "DELETE",
        "/subscriptions/{subscriptionId}".format(subscriptionId='subscription_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 204

def test_update_ncof_events_subscription(client: TestClient):
    """Test case for update_ncof_events_subscription

    Update an existing Individual NCOF Events Subscription
    """
    nncof_events_subscription = nncof_events_subscription = {

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
    # uncomment below to make a request
    response = client.request(
        "PUT",
        "/subscriptions/{subscriptionId}".format(subscriptionId='subscription_id_example'),
        headers=headers,
        json=nncof_events_subscription,
    )

    # uncomment below to assert the status code of the HTTP response
    assert response.status_code == 200
