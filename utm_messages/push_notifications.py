"""
Expo Push Notification utility for ANGA-UTM.

Usage
-----
Single recipient (UserProfile instance)::

    from utm_messages.push_notifications import send_expo_push_notifications
    send_expo_push_notifications(userprofile, "Flight Approved", "Your flight plan has been approved.")

Multiple recipients (UserProfile queryset)::

    from accounts.models import UserProfile
    from utm_messages.push_notifications import send_expo_push_notifications

    pilots = UserProfile.objects.filter(user__role="pilot", user__organization=org)
    send_expo_push_notifications(pilots, "NOTAM Issued", "New NOTAM in your area.", data={"notam_id": 42})
"""

import logging
from itertools import islice

import requests
from django.conf import settings
from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError

logger = logging.getLogger(__name__)

# Expo enforces a maximum of 100 messages per request.
_EXPO_BATCH_SIZE = 100


def _build_session() -> requests.Session:
    """Return a requests Session with the optional Expo access token header."""
    session = requests.Session()
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
    expo_token = getattr(settings, "EXPO_TOKEN", "")
    if expo_token:
        headers["Authorization"] = f"Bearer {expo_token}"
    session.headers.update(headers)
    return session


def send_push_message(token: str, title: str, body: str, extra: dict = None) -> None:
    """
    Send a single Expo push notification.

    Parameters
    ----------
    token:  The recipient's ``ExpoPushToken``.
    title:  Notification title.
    body:   Notification body text.
    extra:  Optional JSON-serialisable dict delivered as ``data`` to the app.
    """
    session = _build_session()
    try:
        response = PushClient(session=session).publish(
            PushMessage(to=token, title=title, body=body, data=extra)
        )
    except PushServerError as exc:
        logger.error(
            "Expo PushServerError sending to %s: %s (errors=%s, response_data=%s)",
            token,
            exc,
            exc.errors,
            exc.response_data,
        )
        raise
    except (ConnectionError, HTTPError) as exc:
        logger.error("Network error sending Expo push to %s: %s", token, exc)
        raise

    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        # The device can no longer receive notifications — clear the stored token.
        from accounts.models import UserProfile  # local import to avoid circular import

        logger.warning("DeviceNotRegistered for token %s — clearing from UserProfile.", token)
        UserProfile.objects.filter(expo_push_token=token).update(expo_push_token=None)
    except PushTicketError as exc:
        logger.error(
            "PushTicketError for token %s: %s (push_response=%s)",
            token,
            exc,
            exc.push_response._asdict(),
        )
        raise


def send_expo_push_notifications(recipients, title: str, body: str, data: dict = None) -> None:
    """
    Send an Expo push notification to one or many UserProfile recipients.

    Parameters
    ----------
    recipients: A single ``UserProfile`` instance **or** a ``UserProfile`` queryset.
                Profiles without an ``expo_push_token`` are silently skipped.
    title:      Notification title.
    body:       Notification body text.
    data:       Optional JSON-serialisable dict delivered to the app.
    """
    from accounts.models import UserProfile  # local import to avoid circular import

    # Normalise a single instance to a queryset.
    if isinstance(recipients, UserProfile):
        recipients = UserProfile.objects.filter(pk=recipients.pk)

    # Only consider profiles that have a token registered.
    tokens = (
        recipients.exclude(expo_push_token__isnull=True)
        .exclude(expo_push_token="")
        .values_list("expo_push_token", flat=True)
    )

    token_list = list(tokens)
    if not token_list:
        logger.debug("send_expo_push_notifications: no tokens found, skipping.")
        return

    # Send in batches to respect Expo's 100-notification-per-request limit.
    it = iter(token_list)
    while True:
        batch = list(islice(it, _EXPO_BATCH_SIZE))
        if not batch:
            break
        for token in batch:
            try:
                send_push_message(token, title, body, extra=data)
            except Exception:
                # Errors are already logged inside send_push_message.
                # Continue processing the remaining tokens in the batch.
                pass
