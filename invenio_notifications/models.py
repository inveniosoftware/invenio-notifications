# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models used for notifications."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Notification(dict):
    """Notification base class."""

    type: str  # event type e.g comment_edit, new_invitation etc
    data: dict  # depending on the type. dump of a record, community, etc.
    trigger: dict  # info about who triggered (and dump thereof), if it was manual or automatic
    timestamp: str  # when the action happened

    def __init__(self, type="", data=None, trigger=None, **kwargs):
        """Constructor."""
        self.type = self["type"] = type
        self.data = self["data"] = data
        self.trigger = self["trigger"] = trigger
        self.timestamp = self["timestamp"] = datetime.now().isoformat()
        self.update(kwargs)

    def dumps(self):
        """Dumps the object as dict."""
        # should have a proper dumper defined, to make sure it is serializable for celery
        d = {k: v for k, v in self.items()}
        d.update(self.__dict__)
        return d

    def copy(self):
        """Returns a copy of this object."""
        return Notification(**self.dumps())


@dataclass
class BackendPayload:
    """Payload base for backend notifications."""

    id: str  # backend id
    kwargs: field(default_factory=dict) = None  # unspecified values for backend


@dataclass
class BackendNotification(Notification):
    """Notification for a single backend.

    Only contains information needed for a backend.
    """

    user: dict  # user dump
    payload: BackendPayload  # backend specific information


@dataclass
class BroadcastRecipient:
    """Broadcast notification recipient.

    Contains user information and which backends should be targeted.
    """

    user: dict  # user dump
    backends: list[BackendPayload]  # backends a user wants to be notified by


@dataclass
class BroadcastNotification(Notification):
    """Notification for broadcasting.

    This should be split into several BackendNotifications.
    """

    recipients: list[
        BroadcastRecipient
    ]  # users and their backends they want to be notified by
