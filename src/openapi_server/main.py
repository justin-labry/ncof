from fastapi import FastAPI

from openapi_server.apis import (
    subscription_transfer_api,
    subscription_transfers_api,
    subscription_api,
    subscriptions_api,
    notifications_api,
)

from .config.app_config import app_config

app = FastAPI(
    title="NCOF Events Subscription",
    description="NCOF Events Subscription Service API. © 2025, 3GPP Organizational Partners (ARIB, ATIS, CCSA, ETSI, TSDSI, TTA, TTC).   All rights reserved. ",
    version="1.0.0",
)

NOTIFICATION_PREFIX = f"/{app_config.notification_prefix}"
SUBSCRIPTION_PREFIX = f"/{app_config.subscription_prefix}"

app.include_router(subscription_transfer_api)
app.include_router(subscription_transfers_api)
app.include_router(subscription_api, prefix=SUBSCRIPTION_PREFIX)
app.include_router(subscriptions_api, prefix=SUBSCRIPTION_PREFIX)
app.include_router(notifications_api, prefix=NOTIFICATION_PREFIX)

print(
    r"""
 _   _  ____ ___  _____
| \ | |/ ___/ _ \|  ___|
|  \| | |  | | | | |_
| |\  | |__| |_| |  _|
|_| \_|\____\___/|_|
"""
)
