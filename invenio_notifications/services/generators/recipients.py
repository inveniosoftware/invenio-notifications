# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Graz University of Technology.
# Copyright (C) 2026 TU Wien.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Recipient generators for notifications."""

from abc import ABC, abstractmethod


class RecipientGenerator(ABC):
    """Recipient generator for a notification."""

    @abstractmethod
    def __call__(self, notification, recipients):
        """Add further recipients for the ``notification`` to the ``recipients``.

        This function takes information from the ``notification`` to add further
        entries to the dictionary of ``recipients``.
        """
        raise NotImplementedError()


class ConditionalRecipientGenerator(RecipientGenerator):
    """Conditional recipient generator for a notification."""

    def __init__(self, then_, else_):
        """Constructor."""
        self.then_ = then_
        self.else_ = else_

    def _condition(self, notification, recipients):
        """The condition to determine which of the recipient generators to use."""
        raise NotImplementedError()

    def __call__(self, notification, recipients):
        """Call applicable generators."""
        generators = (
            self.then_ if self._condition(notification, recipients) else self.else_
        )
        for generator in generators:
            generator(notification, recipients)

        return notification
