# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tasks related to notifications."""

from celery import shared_task

from .models import BackendNotification, BroadcastNotification
from .proxies import current_notifications_manager


@shared_task
def _send_notification_via_backend(backend_notification, backend_id):
    """Task to send notification via backend."""
    current_notifications_manager.notify(backend_notification, backend_id)


@shared_task
def broadcast_notification(broadcast_notification: BroadcastNotification):
    """Task to spawn single notification tasks."""
    for recipient in broadcast_notification.recipients:
        for backend_payload in recipient.backends:
            # only sending needed information to backend
            backend_notification = BackendNotification(
                data=broadcast_notification.data,
                type=broadcast_notification.type,
                trigger=broadcast_notification.trigger,
                timestamp=broadcast_notification.timestamp,
                user=recipient.user,
                payload=backend_payload,
            )
            _send_notification_via_backend.delay(
                backend_notification,
                backend_payload.id,
            )
