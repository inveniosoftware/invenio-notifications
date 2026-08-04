# SPDX-FileCopyrightText: 2023-2025 CERN.
# SPDX-FileCopyrightText: 2023-2026 Graz University of Technology.
# SPDX-FileCopyrightText: 2025 KTH Royal Institute of Technology.
# SPDX-FileCopyrightText: 2026 TU Wien.
# SPDX-License-Identifier: MIT

"""Invenio module for notifications support."""

from .ext import InvenioNotifications
from .proxies import current_notifications, current_notifications_manager

__version__ = "2.0.2"

__all__ = (
    "__version__",
    "current_notifications",
    "current_notifications_manager",
    "InvenioNotifications",
)
