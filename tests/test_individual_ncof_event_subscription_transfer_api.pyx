# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictStr  # noqa: F401
from typing import Any  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.problem_details import ProblemDetails  # noqa: F401
from openapi_server.models.redirect_response import RedirectResponse  # noqa: F401


def test_delete_ncof_event_subscription_transfer(client: TestClient):
    """Test case for delete_ncof_event_subscription_transfer

    Delete an existing Individual NCOF Event Subscription Transfer
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/transfers/{transferId}".format(transferId='transfer_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_ncof_event_subscription_transfer(client: TestClient):
    """Test case for update_ncof_event_subscription_transfer

    Update an existing Individual NCOF Event Subscription Transfer
    """
    body = 'body_example'

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/transfers/{transferId}".format(transferId='transfer_id_example'),
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

