from openapi_server.apis.ncof_events_subscriptions_api_base import BaseNCOFEventsSubscriptionsApi


def get_subscription_service(
) -> BaseNCOFEventsSubscriptionsApi:
    return BaseNCOFEventsSubscriptionsApi.subclasses[0]()
