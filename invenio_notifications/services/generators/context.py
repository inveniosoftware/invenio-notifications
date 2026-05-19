# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
# Copyright (C) 2026 TU Wien.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Context generators for notifications."""

from abc import ABC, abstractmethod

from invenio_records.dictutils import dict_lookup, dict_set

from ...registry import EntityResolverRegistry


class ContextGenerator(ABC):
    """Payload generator for a notification."""

    @abstractmethod
    def __call__(self, notification):
        """Update notification context in-place."""
        raise NotImplementedError()


class EntityResolve(ContextGenerator):
    """Payload generator for a notification using the entity resolvers."""

    def __init__(self, key):
        """Constructor."""
        self.key = key

    def __call__(self, notification):
        """Update required recipient information and add backend ID."""
        entity_ref = dict_lookup(notification.context, self.key)
        entity = EntityResolverRegistry.resolve_entity(entity_ref)
        dict_set(notification.context, self.key, entity)
        return notification
