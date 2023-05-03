# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Generators for notification context."""

from abc import ABC, abstractmethod

from invenio_records.dictutils import dict_lookup, dict_set

from invenio_notifications.backends.email import EmailNotificationBackend
from invenio_notifications.registry import EntityResolverRegistry


class ContextGenerator(ABC):
    """Payload generator for a notification."""

    @abstractmethod
    def __call__(self, notification):
        """Update notification context."""
        raise NotImplementedError()


class RecipientGenerator(ABC):
    """Recipient generator for a notification."""

    @abstractmethod
    def __call__(self, notification, recipients):
        """Add recipients."""
        raise NotImplementedError()


class RecipientBackendGenerator(ABC):
    """Backend generator for a notification."""

    @abstractmethod
    def __call__(self, notification, recipient, backends):
        """Update required recipient information and add backend id."""
        raise NotImplementedError()


class EntityResolve(ContextGenerator):
    """Payload generator for a notification using the entity resolvers."""

    def __init__(self, key):
        """Ctor."""
        self.key = key

    def __call__(self, notification):
        """Update required recipient information and add backend id."""
        entity_ref = dict_lookup(notification.context, self.key)
        entity = EntityResolverRegistry.resolve_entity(entity_ref)
        dict_set(notification.context, self.key, entity)
        return notification


class UserEmailBackend(RecipientBackendGenerator):
    """User related email backend generator for a notification."""

    def __call__(self, notification, recipient, backends):
        """Add backend id to backends."""
        backend_id = EmailNotificationBackend.id
        backends.append(backend_id)
        return backend_id
