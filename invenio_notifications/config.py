# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for notifications support."""

from invenio_i18n import gettext as _

from .backends.email import EmailNotificationBackend

NOTIFICATIONS_DEFAULT_SUBJECT = _("New notification from repository")


class NotificationConfig:
    """Config."""

    backends = {
        EmailNotificationBackend,
    }


NOTIFICATIONS_CONFIG = NotificationConfig
