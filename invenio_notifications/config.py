# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for notifications support."""

from flask_babelex import gettext as _

from .backends.email import EmailNotificationBackend

NOTIFICATIONS_BACKENDS = {
    EmailNotificationBackend,
}

NOTIFICATIONS_DEFAULT_SUBJECT = _("New notification from repository")


class NotificationConfig:
    """Config."""

    backends = NOTIFICATIONS_BACKENDS


NOTIFICATIONS_CONFIG = NotificationConfig
