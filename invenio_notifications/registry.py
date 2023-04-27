# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Entity resolver registry for notifications."""


from invenio_records_resources.references.registry import ResolverRegistryBase

from .proxies import current_notifications


class EntityResolverRegistry(ResolverRegistryBase):
    """Entity Resolver registry for notification context."""

    @classmethod
    def get_registered_resolvers(cls):
        """Get all currently registered resolvers."""
        return iter(current_notifications.entity_resolvers.values())
