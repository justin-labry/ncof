from core.subscription_manager import SubscriptionManager

# from openapi_server.apis.ncof_events_subscriptions_api_base import (
#     BaseNCOFEventsSubscriptionsApi,
# )
# from openapi_server.apis.nwdaf_events_notifications_api_base import (
#     BaseNWDAFEventsNotificationsApi,
# )


# def get_subscription_service() -> BaseNCOFEventsSubscriptionsApi:
#     return BaseNCOFEventsSubscriptionsApi.subclasses[0]()


# def get_notification_service() -> BaseNWDAFEventsNotificationsApi:
#     return BaseNWDAFEventsNotificationsApi.subclasses[0]()


subscription_manager = SubscriptionManager()


def get_subscription_manager() -> SubscriptionManager:
    return subscription_manager
