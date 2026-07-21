# SPDX-FileCopyrightText: 2023-2025 CERN.
# SPDX-FileCopyrightText: 2023-2024 Graz University of Technology.
# SPDX-FileCopyrightText: 2025 KTH Royal Institute of Technology.
# SPDX-License-Identifier: MIT

"""Invenio module for notifications support."""

from .ext import InvenioNotifications
from .proxies import current_notifications, current_notifications_manager

__version__ = "1.3.1"

__all__ = (
    "__version__",
    "current_notifications",
    "current_notifications_manager",
    "InvenioNotifications",
)
