# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023-2024 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Notifications views module."""


from flask import Blueprint
from flask_login import login_required


def create_blueprint(app):
    """Register blueprint routes on app."""
    blueprint = Blueprint(
        "invenio_notifications",
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    return blueprint


def create_blueprint_settings(app):
    """Register blueprint routes on app."""
    blueprint = Blueprint(
        "invenio_notifications_settings",
        __name__,
        template_folder="templates/settings",
        url_prefix="/account/settings/notifications",
        static_folder="static",
    )

    notifications_settings_view_func = app.config[
        "NOTIFICATIONS_SETTINGS_VIEW_FUNCTION"
    ]

    if notifications_settings_view_func:

        @blueprint.route("/", methods=["GET", "POST"])
        @login_required
        def index():
            """View for notification settings."""
            return notifications_settings_view_func()

    return blueprint
