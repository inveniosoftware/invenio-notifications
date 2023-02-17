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
from invenio_records_resources.services.base.config import ConfiguratorMixin, FromConfig

from .backends.email.backend import EmailNotificationBackend


class NotificationConfig(ConfiguratorMixin):
    """Config."""

    backends = FromConfig("NOTIFICATIONS_BACKENDS", {})


# NOTIFICATIONS_CONFIG = NotificationConfig

NOTIFICATIONS_BACKENDS = {
    EmailNotificationBackend.id: EmailNotificationBackend,
}

NOTIFICATIONS_DEFAULT_SUBJECT = _("New notification from repository")
