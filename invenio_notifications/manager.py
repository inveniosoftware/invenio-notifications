# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Notification manager."""

from invenio_notifications.tasks import broadcast_notification, dispatch_notification


class NotificationManager:
    """Notification manager.

    Takes care of building notifications and forwarding them to the backend(s), based
    on the ``NotificationBuilder`` registered for the notification's ``type``.
    """

    def __init__(self, backends, builders):
        """Constructor."""
        self.backends = backends  # via config "NOTIFICATIONS_BACKENDS"
        self.builders = builders  # via config "NOTIFICATIONS_BUILDERS"

    # def validate(self, notification):
    #     """Validate notification object."""
    #     # Validate the type
    #     ...
    #     # Validate context (if possible)
    #     ...

    # Client
    def broadcast(self, notification, eager=False):
        """Broadcast a notification via a background task."""
        self.validate(notification)
        task = broadcast_notification.si(notification.dumps())
        return task.apply() if eager else task.delay()

    # Consumer
    def handle_broadcast(self, notification):
        """Handle a notification broadcast.

        This looks up the configured ``NotificationBuilder`` for the notification's
        type and uses it to resolve the context, build and filter the recipients
        dictionary, and determine the backends to use.
        For each recipient and backend, a background task will be created to dispatch
        the notification.
        """
        builder = self.builders[notification.type]
        # Resolve and expand entities
        builder.resolve_context(notification)
        # Generate recipients
        recipients = builder.build_recipients(notification)
        recipients = builder.filter_recipients(notification, recipients)
        for recipient in recipients.values():
            recipient_backends = builder.build_recipient_backends(
                notification, recipient
            )
            for backend in recipient_backends:
                dispatch_notification.delay(
                    backend,
                    recipient.dumps(),
                    notification.dumps(),
                )

    # Dispatch delivery/sending via a backend
    def handle_dispatch(self, backend_id, recipient, notification):
        """Handle a backend dispatch."""
        self.backends[backend_id].send(notification, recipient)
