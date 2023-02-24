# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Notification backend base class used for notifications."""

from abc import ABC, abstractmethod


class NotificationBackend(ABC):
    """Base class for notification backends."""

    id = None
    """Unique id of the backend."""

    @abstractmethod
    def send_notification(notification, **kwargs):
        """Here each concrete implementation shall dispatch notification message."""
        raise NotImplementedError()
