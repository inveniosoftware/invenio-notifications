# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""E-mail specific notification backend."""

from celery import shared_task
from flask import current_app
from flask_babelex import gettext as _

from invenio_notifications.backends.base import NotificationBackend
from invenio_notifications.backends.utils.loaders import JinjaTemplateLoaderMixin


class EmailNotificationBackend(NotificationBackend, JinjaTemplateLoaderMixin):
    """Email specific notification backend."""

    id = "email"

    @shared_task
    def send_notification(notification):
        """Construct and send email."""
        from invenio_mail.tasks import send_email

        mail_data = {}
        mail_data["recipients"] = [r["email"] for r in notification["recipients"]]
        mail_data["html"] = notification["html_body"]
        mail_data["body"] = notification["text_body"]
        mail_data["subject"] = notification["subject"]
        mail_data["sender"] = notification["sender"]
        send_email(mail_data)

    def extend_notification(self, notification):
        """Notification will be a deep copy."""
        tpl_html = self.get_template(notification["type"] + ".html")
        tpl_txt = self.get_template(notification["type"] + ".txt")

        notification["html_body"] = tpl_html.render(notification=notification)
        notification["text_body"] = tpl_txt.render(notification=notification)
        notification["subject"] = notification.get(
            "subject", current_app.config["NOTIFICATIONS_DEFAULT_SUBJECT"]
        )
        notification["sender"] = current_app.config["SECURITY_EMAIL_SENDER"]
        return notification
