# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for notifications support."""

from .ext import InvenioNotifications

__version__ = "0.1.0"

__all__ = (
    "__version__",
    "InvenioNotifications",
)
