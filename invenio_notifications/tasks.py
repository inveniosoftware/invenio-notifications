# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Tasks related to notifications."""

from celery import shared_task

from invenio_notifications.models import Notification, Recipient

from .proxies import current_notifications_manager


@shared_task
def broadcast_notification(notification):
    """Handles a notification broadcast."""
    current_notifications_manager.handle_broadcast(Notification(**notification))


@shared_task(max_retries=5, default_retry_delay=5 * 60)
def dispatch_notification(backend, recipient, notification):
    """Dispatches a notification to a recipient for a specific backend."""
    current_notifications_manager.handle_dispatch(
        backend, Recipient(**recipient), Notification(**notification)
    )
