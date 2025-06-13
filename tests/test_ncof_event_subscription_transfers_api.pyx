# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import StrictStr  # noqa: F401
from typing import Any  # noqa: F401
from openapi_server.models.problem_details import ProblemDetails  # noqa: F401


def test_create_ncof_event_subscription_transfer(client: TestClient):
    """Test case for create_ncof_event_subscription_transfer

    Provide information about requested analytics subscriptions transfer and potentially create a new Individual NCOF Event Subscription Transfer resource.
    """
    body = 'body_example'

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/transfers",
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

