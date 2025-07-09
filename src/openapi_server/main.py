from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from openapi_server.apis import (
    subscription_transfer_api,
    subscription_transfers_api,
    subscription_api,
    subscriptions_api,
    notifications_api,
)

from config.app_config import app_config

print(
    r"""
 _   _  ____ ___  _____
| \ | |/ ___/ _ \|  ___|
|  \| | |  | | | | |_
| |\  | |__| |_| |  _|
|_| \_|\____\___/|_|
"""
)

app = FastAPI(
    title="NCOF Events Subscription",
    description="NCOF Events Subscription Service API. © 2025, 3GPP Organizational Partners (ARIB, ATIS, CCSA, ETSI, TSDSI, TTA, TTC).   All rights reserved. ",
    version="1.0.0",
)

app.mount("/public", StaticFiles(directory="public"), name="public")


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("public/index.html")


NOTIFICATION_PREFIX = f"/{app_config.notification_prefix}"
SUBSCRIPTION_PREFIX = f"/{app_config.subscription_prefix}"

app.include_router(subscription_transfer_api)
app.include_router(subscription_transfers_api)
app.include_router(subscription_api, prefix=SUBSCRIPTION_PREFIX)
app.include_router(subscriptions_api, prefix=SUBSCRIPTION_PREFIX)
app.include_router(notifications_api, prefix=NOTIFICATION_PREFIX)
