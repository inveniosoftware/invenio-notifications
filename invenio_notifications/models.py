# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models used for notifications."""

from dataclasses import asdict, dataclass


@dataclass
class Notification:
    """Notification base class."""

    type: str  # event type e.g comment_edit, new_invitation etc
    context: dict  # depending on the type. dump of a record, community, etc.

    # TODO: We might be able to get away with a JSON encoder/decoder instead:
    #   https://stackoverflow.com/a/51286749
    def dumps(self):
        """Dumps the object as dict."""
        return {
            "type": self.type,
            "context": self.context,
        }


@dataclass
class Recipient:
    """Broadcast notification recipient.

    Contains user information.
    """

    data: dict  # user dump

    def dumps(self):
        """Dumps the object as dict."""
        return asdict(self)
