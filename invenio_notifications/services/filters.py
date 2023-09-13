# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Filters for notification recipients."""

from abc import ABC, abstractmethod

from invenio_records.dictutils import dict_lookup


class RecipientFilter(ABC):
    """Recipient filter for a notification."""

    @abstractmethod
    def __call__(self, notification, recipients):
        """Filter recipients."""
        raise NotImplementedError()


class KeyRecipientFilter(RecipientFilter):
    """Recipient filter based on a given key."""

    def __init__(self, key):
        """Initialize with key for lookup."""
        super().__init__()
        self._key = key

    def __call__(self, notification, recipients):
        """Filter recipients."""
        recipient_key = dict_lookup(notification.context, self._key)
        if not isinstance(recipient_key, str):
            return recipients

        if recipient_key in recipients:
            del recipients[recipient_key]

        return recipients
