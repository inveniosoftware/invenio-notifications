# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Builderes for notifications."""

from abc import ABC, abstractmethod

from invenio_notifications.services.filters import RecipientFilter
from invenio_notifications.services.generators import (
    ContextGenerator,
    RecipientBackendGenerator,
    RecipientGenerator,
)


class NotificationBuilder(ABC):
    """Base notification builder."""

    context: list[ContextGenerator]
    recipients: list[RecipientGenerator]
    recipient_filters: list[RecipientFilter]
    recipient_backends: list[RecipientBackendGenerator]

    type = "Notification"

    @classmethod
    @abstractmethod
    def build(cls, **kwargs):
        """Build notification based on type and additional context."""
        raise NotImplementedError()

    @classmethod
    def resolve_context(cls, notification):
        """Resolve all references in the notification context."""
        for ctx_func in cls.context:
            # NOTE: We assume that the notification is mutable and modified in-place
            ctx_func(notification)
        return notification

    @classmethod
    def build_recipients(cls, notification):
        """Return a dictionary of unique recipients for the notification."""
        recipients = {}
        for recipient_func in cls.recipients:
            recipient_func(notification, recipients)
        return recipients

    @classmethod
    def filter_recipients(cls, notification, recipients):
        """Apply filters to the recipients."""
        for recipient_filter_func in cls.recipient_filters:
            recipient_filter_func(notification, recipients)
        return recipients

    @classmethod
    def build_recipient_backends(cls, notification, recipient):
        """Return the backends for recipient."""
        backends = []
        for recipient_backend_func in cls.recipient_backends:
            recipient_backend_func(notification, recipient, backends)
        return backends
