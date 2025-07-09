import logging
import uvicorn
import asyncio
import signal

from fastapi import FastAPI

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from config.app_config import app_config
from openapi_server.apis import (
    notifications_api,
    subscription_api,
    subscription_transfer_api,
    subscription_transfers_api,
    subscriptions_api,
)

print(
    r"""
 _   _  ____ ___  _____
| \ | |/ ___/ _ \|  ___|
|  \| | |  | | | | |_
| |\  | |__| |_| |  _|
|_| \_|\____\___/|_|
"""
)


# 생명주기 이벤트 핸들러
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="NCOF Events Subscription",
    description="NCOF Events Subscription Service API. © 2025, 3GPP Organizational Partners (ARIB, ATIS, CCSA, ETSI, TSDSI, TTA, TTC).   All rights reserved. ",
    version="1.0.0",
    lifespan=lifespan,
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


class QuietUvicornServer:
    def __init__(self, config):
        self.config = config
        self.server = uvicorn.Server(config)
        self.should_exit = False

    def handle_exit(self, sig, frame):
        print("\n정상 종료 중...")
        self.should_exit = True
        self.server.should_exit = True

    async def serve(self):
        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)

        try:
            await self.server.serve()
        except Exception:
            pass  # 종료 시 예외 무시
        finally:
            print("서버 종료 완료")


if __name__ == "__main__":
    config = uvicorn.Config(
        "openapi_server.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_config="log_config.ini",
    )

    server = QuietUvicornServer(config)
    logging.info(f"server port:{8080}")
    try:

        asyncio.run(server.serve())
    except KeyboardInterrupt:
        pass
