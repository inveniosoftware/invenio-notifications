# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for notifications support."""

from invenio_i18n import gettext as _
from invenio_records_resources.services.base.config import ConfiguratorMixin, FromConfig


NOTIFICATIONS_BACKENDS = {}
"""Notification backends.

NOTIFICATIONS_BACKENDS = {
    "email": EmailBackend,
    "cern": CERNNotificationsBackend,
    "slack": SlackBackend,
}
"""

NOTIFICATIONS_BUILDERS = {}
"""Notification builders.

NOTIFICATIONS_BUILDERS = {
    "community_submission_create": CommunitySubmissionCreate,
    "community_submission_accept": CommunitySubmissionAccept,
    "community_submission_reject": CommunitySubmissionReject,
    "member_invitation_create": CommunityMemberInvitationCreate,
    "member_invitation_accept": CommunityMemberInvitationAccept,
    "member_invitation_reject": CommunityMemberInvitationReject,
    "request_comment_create": RequestCommentCreate,
}
"""

NOTIFICATIONS_ENTITY_RESOLVERS = []
"""List of entity resolvers used by notification builders."""


class NotificationConfig(ConfiguratorMixin):
    """Config."""

    backends = FromConfig("NOTIFICATIONS_BACKENDS", NOTIFICATIONS_BACKENDS)
    builders = FromConfig("NOTIFICATIONS_BUILDERS", NOTIFICATIONS_BACKENDS)


NOTIFICATIONS_CONFIG = NotificationConfig
