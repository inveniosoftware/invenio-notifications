# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
# Copyright (C) 2026 TU Wien.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Generators for notification context."""

from .backends import EmailBackendGenerator, RecipientBackendGenerator, UserEmailBackend
from .context import ContextGenerator, EntityResolve, EntityResolverContextGenerator
from .recipients import ConditionalRecipientGenerator, RecipientGenerator

__all__ = (
    "ConditionalRecipientGenerator",
    "ContextGenerator",
    "EmailBackendGenerator",
    "EntityResolve",
    "EntityResolverContextGenerator",
    "RecipientBackendGenerator",
    "RecipientGenerator",
    "UserEmailBackend",
)
