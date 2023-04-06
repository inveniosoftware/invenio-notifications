# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models used for notifications."""

from dataclasses import asdict, dataclass, field


@dataclass
class Notification:
    """Notification base class."""

    type: str  # event type e.g comment_edit, new_invitation etc
    context: dict  # depending on the type. dump of a record, community, etc.

    # TODO: We might be able to get away with a JSON encoder/decoder instead:
    #   https://stackoverflow.com/a/51286749
    def asdict(self):
        """Dumps the object as dict."""
        return asdict(self)


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
