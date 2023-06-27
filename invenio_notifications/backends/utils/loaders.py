# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Template loaders for notification backend."""

from flask import current_app
from invenio_i18n import force_locale, get_locale
from invenio_i18n.proxies import current_i18n


class JinjaTemplateLoaderMixin:
    """Used only in NotificationBackend classes."""

    template_folder = "invenio_notifications"

    def render_template(self, notification, recipient):
        """Render template for a notification.

        Fetch the template based on the notification type and return the template blocks.
        More specific templates take precedence over less specific ones.
        Rendered template will also take the locale into account.
        """
        # Take recipient locale into account. Fallback to default locale (set via config variable)
        locale = recipient.data.get("preferences", {}).get("locale")
        if not current_i18n.is_locale_available(locale):
            locale = get_locale()

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
            },
        )

        # Forcing the locale of the recipient so the correct language is chosen for translatable strings
        with force_locale(locale):
            # "Force" rendering the whole template (including global variables).
            # Since we render block by block afterwards, the context and variables
            # would be lost between blocks.
            list(template.root_render_func(ctx))

            return {
                block: "".join(
                    block_func(ctx)
                )  # have to evaluate, as block_func is a generator
                for block, block_func in template.blocks.items()
            }
