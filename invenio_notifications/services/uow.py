# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Unit of work for notifications."""

from invenio_records_resources.services.uow import Operation

from ..tasks import broadcast_notification


class NotificationOp(Operation):
    """A notification operation."""

    def __init__(self, notification):
        """Initialize operation."""
        self._notification = notification

    def on_post_commit(self, uow):
        """Start task to send notification."""
        broadcast_notification.delay(self._notification.dumps())
