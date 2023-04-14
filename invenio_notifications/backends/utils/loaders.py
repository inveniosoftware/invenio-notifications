# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Template loaders for notification backend."""

from flask import current_app

from invenio_notifications.models import Notification, Recipient


class JinjaTemplateLoaderMixin:
    """Used only in NotificationBackend classes."""

    template_folder = "invenio_notifications"

    def render_template(self, notification: Notification, recipient: Recipient):
        # Take locale into account
        locale = recipient.data.get("locale", "en")
        template = current_app.jinja_env.select_template(
            [
                # Backend-specific templates first, e.g notifications/email/comment_edit.jinja
                f"{self.template_folder}/{self.id}/{notification.type}.{locale}.jinja",
                f"{self.template_folder}/{self.id}/{notification.type}.jinja",
                # Default templates, e.g notifications/comment_edit.jinja
                f"{self.template_folder}/{notification.type}.{locale}.jinja",
                f"{self.template_folder}/{notification.type}.jinja",
            ]
        )
        ctx = template.new_context(
            {
                "notification": notification,
                "recipient": recipient,
            }
        )
        return {
            block: "".join(
                block_func(ctx)
            )  # have to evaluate, as block_func is a generator
            for block, block_func in template.blocks.items()
        }
