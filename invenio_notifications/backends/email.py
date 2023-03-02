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

    def send_notification(self, backend_notification, **kwargs):
        """Construct and send email."""
        tpl_html = self.get_template(backend_notification["type"] + ".html")
        tpl_txt = self.get_template(backend_notification["type"] + ".txt")

        subject = backend_notification.get(
            "subject", current_app.config["NOTIFICATIONS_DEFAULT_SUBJECT"]
        )

        mail_data = {}
        mail_data["recipients"] = [backend_notification.get("payload", {}).get("to")]
        mail_data["html"] = tpl_html.render(notification=backend_notification)
        mail_data["body"] = tpl_txt.render(notification=backend_notification)
        mail_data["subject"] = subject
        mail_data["sender"] = current_app.config["MAIL_DEFAULT_SENDER"]
        send_email(mail_data)
