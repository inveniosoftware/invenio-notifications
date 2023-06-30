# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Errors used in notification system."""


class NotificationError(Exception):
    """General notification."""


class NotificationBackendNotFoundError(NotificationError):
    """The provided backend is not configured."""

    def __init__(self, backend_id):
        """Constructor.

        :param backend_id: The id of the backend.
        """
        super().__init__(
            "Notification backend `{id}` is not registered.".format(id=backend_id)
        )


class NotificationBackendAlreadyRegisteredError(NotificationError):
    """The provided backend is not configured."""

    def __init__(self, backend_id):
        """Constructor.

        :param backend_id: The id of the backend.
        """
        super().__init__(
            "Notification backend `{id}` already registered.".format(id=backend_id)
        )
