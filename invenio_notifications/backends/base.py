# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Notification backend base class."""

from abc import ABC, abstractmethod


class NotificationBackend(ABC):
    """Base class for notification backends."""

    id = None
    """Unique id of the backend."""

    @abstractmethod
    def send(self, notification, recipient):
        """Send the notification message."""
        raise NotImplementedError()
