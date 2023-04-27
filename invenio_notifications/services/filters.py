# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Filters for notification recipients."""

from abc import ABC, abstractmethod


class RecipientFilter(ABC):
    """Recipient filter for a notification."""

    @abstractmethod
    def __call__(self, notification, recipients):
        """Filter recipients."""
        raise NotImplementedError()
