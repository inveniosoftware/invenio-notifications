# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
# Copyright (C) 2026 TU Wien.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Backend generators for notifications."""

from abc import ABC, abstractmethod

from invenio_notifications.backends.email import EmailNotificationBackend


class RecipientBackendGenerator(ABC):
    """Backend generator for a notification."""

    @abstractmethod
    def __call__(self, notification, recipient, backends):
        """Update required recipient information and add backend ID."""
        raise NotImplementedError()


class UserEmailBackend(RecipientBackendGenerator):
    """Backend generator for adding the email backend."""

    def __call__(self, notification, recipient, backends):
        """Add email backend ID to backends."""
        backend_id = EmailNotificationBackend.id
        backends.append(backend_id)
        return backend_id
