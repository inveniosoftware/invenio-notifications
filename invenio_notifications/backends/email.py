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

from invenio_notifications.backends.base import NotificationBackend
from invenio_notifications.backends.utils.loaders import JinjaTemplateLoaderMixin


class EmailNotificationBackend(NotificationBackend, JinjaTemplateLoaderMixin):
    """Email specific notification backend."""

    id = "email"

    def send(self, notification, recipient):
        """Mail sending implementation."""
        content = self.render_template(notification, recipient)

        resp = send_email(
            {
                "subject": content["subject"],
                "html": content["html_body"],
                "body": content["plain_body"],
                "recipients": [
                    recipient.data.get("email") or recipient.data.get("email_hidden")
                ],
                "sender": current_app.config["MAIL_DEFAULT_SENDER"],
            }
        )
        return resp  # TODO: what would a "delivery" result be
