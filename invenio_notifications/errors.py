# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Errors used in notification system."""

from flask_babelex import gettext as _


class NotificationError(Exception):
    """General notification."""


class NotificationTypeNotFoundError(NotificationError):
    """The provided event type is not configured."""

    def __init__(self, type):
        """Constructor.

        :param type: The name of the event type.
        """
        super().__init__(_("Notification type `{}` not configured.".format(type)))


class NotificationBackendNotFoundError(NotificationError):
    """The provided backend is not configured."""

    def __init__(self, backend_id, type_=None):
        """Constructor.

        :param backend_id: The id of the backend.
        :param type: The name of the event type.
        """
        type_text = _(" for type `{}` ").format(type_) if type_ else ""
        super().__init__(
            _(
                "Notification backend `{}`{}is not registered.".format(
                    backend_id, type_text
                )
            )
        )


class NotificationBackendAlreadyRegisteredError(NotificationError):
    """The provided backend is not configured."""

    def __init__(self, backend_id):
        """Constructor.

        :param event_type: The id of the backend.
        """
        super().__init__(
            _("Notification backend `{}` already registered.".format(backend_id))
        )
