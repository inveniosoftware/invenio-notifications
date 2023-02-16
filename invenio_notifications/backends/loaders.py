# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Template loaders for notification backend."""

from flask import current_app
from jinja2 import TemplateNotFound, TemplatesNotFound


class JinjaTemplateLoaderMixin:
    """Used only in NotificationBackend classes."""

    template_folder = "invenio_notifications"

    def _load_template(self, path):
        try:
            template = current_app.jinja_env.get_template(path)
        except TemplateNotFound:
            template = None

        return template

    def get_template(self, name):
        """Retrieves a template from the template folder."""
        # e.g /notifications/email/comment_edit.html
        base_template_path = f"{self.template_folder}/{name}"
        specific_template_path = f"{self.template_folder}/{self.id}/{name}"

        base_template = self._load_template(base_template_path)
        specific_template = self._load_template(specific_template_path)

        if not specific_template and not base_template:
            raise TemplatesNotFound(names=[base_template_path, specific_template_path])

        return specific_template or base_template
