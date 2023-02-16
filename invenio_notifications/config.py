# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for notifications support."""

from flask_babelex import gettext as _
from invenio_records_resources.services.base.config import ConfiguratorMixin, FromConfig

from .backends.email.backend import EmailNotificationBackend
from .events import (
    CommunityInvitationAcceptedEvent,
    CommunityInvitationCreatedEvent,
    CommunityInvitationDeclinedEvent,
    CommunitySubmissionCreatedEvent,
    CommunitySubmissionDeclinedEvent,
    CommunitySubmissionDeletedEvent,
    CommunitySubmissionSubmittedEvent,
)


class NotificationConfig(ConfiguratorMixin):
    """Config."""

    backends = FromConfig("NOTIFICATIONS_BACKENDS", {})
    notification_policy = FromConfig("NOTIFICATIONS_POLICY", {})


# NOTIFICATIONS_CONFIG = NotificationConfig

NOTIFICATIONS_BACKENDS = {
    EmailNotificationBackend.id: EmailNotificationBackend,
}

NOTIFICATIONS_DEFAULT_SUBJECT = _("New notification from repository")

NOTIFICATIONS_POLICY = {
    CommunitySubmissionSubmittedEvent.handling_key: {
        "backends": [
            EmailNotificationBackend.id,
        ],
    },
    CommunitySubmissionCreatedEvent.handling_key: {
        "backends": [
            EmailNotificationBackend.id,
            # 'text',
        ],
    },
    CommunitySubmissionDeclinedEvent.handling_key: {
        "backends": [
            EmailNotificationBackend.id,
            # 'text',
        ],
    },
    CommunitySubmissionDeletedEvent.handling_key: {
        "backends": [
            EmailNotificationBackend.id,
            # 'text',
        ],
    },
    "comment_created": {
        "backends": [
            EmailNotificationBackend.id,
            # 'slack',
        ],
        # 'recipients': []
    },
    "invitation_expired": {"backends": []},
    CommunityInvitationCreatedEvent.handling_key: {
        "backends": [
            EmailNotificationBackend.id,
        ],
    },
    CommunityInvitationAcceptedEvent.handling_key: {
        "backends": [
            EmailNotificationBackend.id,
        ],
    },
    CommunityInvitationDeclinedEvent.handling_key: {
        "backends": [
            EmailNotificationBackend.id,
        ],
    },
}
