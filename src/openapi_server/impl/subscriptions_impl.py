# import uuid

# import json

# from openapi_server.apis.individual_ncof_events_subscription_api_base import (
#     BaseIndividualNCOFEventsSubscriptionApi,
# )
# from openapi_server.apis.ncof_events_subscriptions_api_base import (
#     BaseNCOFEventsSubscriptionsApi,
# )
# from openapi_server.config.app_config import AppConfig
# from openapi_server.models.nncof_events_subscription import NncofEventsSubscription

# # HOST = app_config.host
# # PORT = app_config.port
# # SERVER_IP = app_config.server_ip


# class SubscriptionNotFoundError(Exception):
#     pass


# class NCOFEventSubscriptionsImpl(
#     BaseNCOFEventsSubscriptionsApi, BaseIndividualNCOFEventsSubscriptionApi
# ):
#     def __init__(self, app_config: AppConfig):
#         self.app_config = app_config

#     def get_ncof_notification_uri(self, subscription_id: str) -> str:
#         return f"http://{self.app_config.host}:{self.app_config.port}/ETRI_INRS_TEAM/Nsmf_EventExposure/1.0.0/notifications/{subscription_id}"

#     async def create_ncof_events_subscription(
#         self,
#         nncof_events_subscription: NncofEventsSubscription,
#     ):
#         print(nncof_events_subscription)
#         print(
#             json.dumps(
#                 nncof_events_subscription.model_dump(), indent=2, ensure_ascii=False
#             )
#         )
#         return "subscription-0001"

#     async def delete_ncof_events_subscription(self, subscription_id: str) -> None: ...

#     async def update_ncof_events_subscription(
#         self,
#         subscription_id: str,
#         nncof_events_subscription: NncofEventsSubscription,
#     ) -> NncofEventsSubscription: ...
