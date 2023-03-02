# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tasks related to notifications."""

from celery import shared_task

from .models import BackendNotification
from .proxies import current_notifications_manager


@shared_task
def send_notification_via_backend(backend_notification, backend_id):
    """Task to send notification via backend."""
    current_notifications_manager.notify_backend(backend_notification, backend_id)


@shared_task
def broadcast(broadcast_notification):
    """Task to spawn single notification tasks."""
    for recipient in broadcast_notification.get("recipients", []):
        for backend_payload in recipient.get("backends", []):
            # only sending needed information to backend
            backend_notification = BackendNotification(
                data=broadcast_notification.get("data", {}),
                type=broadcast_notification.get("type", ""),
                trigger=broadcast_notification.get("trigger", {}),
                timestamp=broadcast_notification.get("timestamp", ""),
                user=recipient.get("user", {}),
                payload=backend_payload,
            )
            send_notification_via_backend.delay(
                backend_notification.dumps(),
                backend_payload.get("id", ""),
            )
