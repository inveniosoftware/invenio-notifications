# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for notifications support."""

NOTIFICATIONS_BACKENDS = {}
"""Notification backends.

.. code-block::python

    NOTIFICATIONS_BACKENDS = {
        "email": EmailBackend,
        "cern": CERNNotificationsBackend,
        "slack": SlackBackend,
    }
"""

NOTIFICATIONS_BUILDERS = {}
"""Notification builders.

.. code-block::python

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
"""List of entity resolvers used by notification builders.

.. code-block::python

    NOTIFICATIONS_ENTITY_RESOLVERS = [
        UserResultItemResolver(),
        RDMRecordResultItemResolver(),
        CommunityResultItemResolver(),
        RequestResultItemResolver(),
        RequestEventResultItemResolver(),
    ]
"""

NOTIFICATIONS_SETTINGS_VIEW_FUNCTION = None
"""View function for notification settings.

This should be set higher up in the module hierarchy (e.g. invenio-app-rdm), as
this module does not have knowledge of the settings view.
"""

NOTIFICATIONS_GROUP_EMAIL_DOMAIN = None
"""Domain suffix to append to group names when email is not provided.

When a recipient is a group and has no email or email_hidden field, the group's
name will be used as the email address with this domain appended.

Example:
    NOTIFICATIONS_GROUP_EMAIL_DOMAIN = "cern.ch"
    # Group "physics-team" becomes "physics-team@cern.ch"

Set to None to disable domain formatting (groups must have email field set).
"""
