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
)


class NotificationManager:
    """Notification manager taking care of backends sending notifications."""

    def __init__(self, config):
        """Constructor."""
        self._config = config
        self._backends = {}

    def _backend_exists(self, backend_id):
        """Check if backend is registered."""
        return backend_id in self._backends

    def _dispatch_notification(self, notification, backend, **kwargs):
        """Extend notification and start task for sending."""
        try:
            extended_notification = backend.extend_notification(
                notification.copy(), **kwargs
            )

            backend.send_notification.apply_async(
                args=[extended_notification.dumps()],
            )

        except Exception as e:
            current_app.logger.warning(e)
            raise e

    def broadcast(self, notification, **kwargs):
        """Broadcast notification to backends."""
        for backend in self._backends.values():
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
