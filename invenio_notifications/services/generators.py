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
        """Update notification context in-place."""
        raise NotImplementedError()


class RecipientGenerator(ABC):
    """Recipient generator for a notification."""

    @abstractmethod
    def __call__(self, notification, recipients):
        """Add further recipients for the ``notification`` to the ``recipients``.

        This function takes information from the ``notification`` to add further
        entries to the dictionary of ``recipients``.
        """
        raise NotImplementedError()


class ConditionalRecipientGenerator(RecipientGenerator):
    """Conditional recipient generator for a notification."""

    def __init__(self, then_, else_):
        """Constructor."""
        self.then_ = then_
        self.else_ = else_

    def _condition(self, notification, recipients):
        """The condition to determine which of the recipient generators to use."""
        raise NotImplementedError()

    def __call__(self, notification, recipients):
        """Call applicable generators."""
        generators = (
            self.then_ if self._condition(notification, recipients) else self.else_
        )
        for generator in generators:
            generator(notification, recipients)

        return notification


class RecipientBackendGenerator(ABC):
    """Backend generator for a notification."""

    @abstractmethod
    def __call__(self, notification, recipient, backends):
        """Update required recipient information and add backend ID."""
        raise NotImplementedError()


class EntityResolve(ContextGenerator):
    """Payload generator for a notification using the entity resolvers."""

    def __init__(self, key):
        """Constructor."""
        self.key = key

    def __call__(self, notification):
        """Update required recipient information and add backend ID."""
        entity_ref = dict_lookup(notification.context, self.key)
        if entity_ref is None:
            return notification
        entity = EntityResolverRegistry.resolve_entity(entity_ref)
        dict_set(notification.context, self.key, entity)
        return notification


class UserEmailBackend(RecipientBackendGenerator):
    """Backend generator for adding the email backend."""

    def __call__(self, notification, recipient, backends):
        """Add email backend ID to backends."""
        backend_id = EmailNotificationBackend.id
        backends.append(backend_id)
        return backend_id
