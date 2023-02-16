# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Initialization used for notifications."""


from flask import current_app

from .errors import (
    NotificationBackendAlreadyRegisteredError,
    NotificationBackendNotFoundError,
    NotificationTypeNotFoundError,
)


class NotificationManager:
    """Notification manager taking care of backends sending notifications."""

    def __init__(self, config):
        """Constructor."""
        self._config = config
        self._backends = {}
        self._notification_policy = config.notification_policy

    def _backend_exists(self, backend_id):
        """Check if backend is registered."""
        return backend_id in self._backends

    def validate_policy(self):
        """Validate policy to make sure no backend is used without being specified."""
        for event_type, event_policy in self._notification_policy.items():
            backend_ids = event_policy.get("backends", [])
            for backend_id in backend_ids:
                if not self._backend_exists(backend_id):
                    raise NotificationBackendNotFoundError(backend_id, type_=event_type)

    def _dispatch_notification(self, notification, backend, **kwargs):
        """Extend notification and start task for sending."""
        try:
            extended_notification = backend.extend_notification(
                notification.copy(), **kwargs
            )

            # These do not always get logged
            backend.send_notification.apply_async(
                args=[extended_notification.dumps()],
            )

        except Exception as e:
            current_app.logger.warning(e)
            raise e

    def broadcast(self, notification, **kwargs):
        """Broadcast notification to backends according to event policy."""
        event_policy = self._notification_policy.get(notification.type)
        if event_policy is None:
            current_app.logger.warning(NotificationTypeNotFoundError(notification.type))
            return

        for backend_id in event_policy.get("backends", []):
            backend = self._backends.get(backend_id)
            if backend is None:
                current_app.logger.warning(
                    NotificationBackendNotFoundError(
                        backend_id, type_=notification.type
                    )
                )
                continue

            self._dispatch_notification(notification, backend, **kwargs)

    def notify(self, notification, backend_id, **kwargs):
        """Set message and notify specific backend.

        Will pass the key for the specific backend to notify.
        """
        backend = self._backends.get(backend_id)
        if backend is None:
            current_app.logger.warning(NotificationBackendNotFoundError(backend_id))
            return

        self._dispatch_notification(notification, backend, **kwargs)

    def register(self, backend):
        """Register backend in manager."""
        if self._backend_exists(backend.id):
            raise NotificationBackendAlreadyRegisteredError(backend.id)
        self._backends[backend.id] = backend

    def deregister(self, backend):
        """Deregister backend in manager."""
        del self._backends[backend.id]

    def register_event(self, event, event_config):
        """Register event with config.

        Other modules should be able to register their own events and specify a policy.
        """
        event_name = event.handling_key
        if self._notification_policy.has_key(event_name):
            return

        policy = {
            "backends": event_config.get("backends", []),
        }

        for backend_id in policy.get("backends"):
            if not self._backend_exists(backend_id):
                raise NotificationBackendNotFoundError(backend_id)

        self._notification_policy[event_name] = policy
