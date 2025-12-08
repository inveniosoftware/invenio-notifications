# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""E-mail specific notification backend."""

from flask import current_app
from invenio_mail.tasks import send_email
from marshmallow_utils.html import strip_html

from invenio_notifications.backends.base import NotificationBackend
from invenio_notifications.backends.utils.loaders import JinjaTemplateLoaderMixin


class EmailNotificationBackend(NotificationBackend, JinjaTemplateLoaderMixin):
    """Email specific notification backend."""

    id = "email"

    def _resolve_email(self, recipient):
        """Resolve email address for recipient with proper domain handling.

        Resolution order:
        1. Use explicit email field if present
        2. Use email_hidden field if present
        3. For groups: format name with domain (if configured)
        4. Fallback to name as-is (for backward compatibility)

        Args:
            recipient: Recipient object with data dict

        Returns:
            str: Resolved email address or None if no email can be determined
        """
        # Try explicit email fields first
        email = recipient.data.get("email") or recipient.data.get("email_hidden")

        if email:
            return email

        # Fallback to name-based email
        name = recipient.data.get("name")

        if not name:
            return None

        # If name already contains @, assume it's a valid email
        if "@" in name:
            return name

        # Check if domain formatting is configured
        domain = current_app.config.get("NOTIFICATIONS_GROUP_EMAIL_DOMAIN")

        # Format with domain if configured, otherwise use name as-is
        if domain:
            return f"{name}@{domain}"

        # Backward compatibility: return name without domain
        return name

    def send(self, notification, recipient):
        """Mail sending implementation."""
        # Resolve email with proper domain handling for groups
        email = self._resolve_email(recipient)

        # Handle case where email cannot be determined
        if not email:
            # Log warning and skip sending
            current_app.logger.warning(
                f"Cannot send email notification: no email address found for recipient. "
                f"Recipient data: {recipient.data}"
            )
            return None

        content = self.render_template(notification, recipient)

        resp = send_email(
            {
                "subject": content["subject"],
                "html": content["html_body"],
                "body": strip_html(content["plain_body"]),
                "recipients": [email],
                "sender": current_app.config["MAIL_DEFAULT_SENDER"],
                "reply_to": current_app.config["MAIL_DEFAULT_REPLY_TO"],
            }
        )
        return resp
