# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Notifications base backend module."""

from .builders import NotificationBuilder
from .filters import KeyRecipientFilter, RecipientFilter
from .generators import (
    ConditionalRecipientGenerator,
    ContextGenerator,
    EmailBackendGenerator,
    EntityResolverContextGenerator,
    RecipientBackendGenerator,
    RecipientGenerator,
)

__all__ = (
    "ConditionalRecipientGenerator",
    "ContextGenerator",
    "EmailBackendGenerator",
    "EntityResolverContextGenerator",
    "KeyRecipientFilter",
    "NotificationBuilder",
    "RecipientBackendGenerator",
    "RecipientFilter",
    "RecipientGenerator",
)
