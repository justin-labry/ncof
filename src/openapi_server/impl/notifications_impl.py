# import json

# from openapi_server.apis.nwdaf_events_notifications_api_base import (
#     BaseNWDAFEventsNotificationsApi,
# )
# from openapi_server.models.event_notification import EventNotification


# class EventNotificationImpl(BaseNWDAFEventsNotificationsApi):
#     """
#     Subscription service for NWDAF events notifications.
#     """

#     async def create_nwdaf_events_notification(
#         self,
#         subscription_id: str,
#         event_notification: EventNotification,
#     ) -> None:
#         """
#         Create a subscription for NWDAF events notifications.

#         Args:
#             event_notification (EventNotification): The event notification to be created.

#         Returns:
#             None
#         """
#         print(f"subscription_id: {subscription_id}")
#         print(json.dumps(event_notification.model_dump(), indent=2))
