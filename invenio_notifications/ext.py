# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2023-2024 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for notifications support."""


from flask_menu import current_menu
from importlib_metadata import entry_points
from invenio_i18n import LazyString
from invenio_i18n import lazy_gettext as _
from invenio_theme.proxies import current_theme_icons

from . import config
from .manager import NotificationManager


class InvenioNotifications(object):
    """Invenio-Notifications extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_manager(app)
        self.init_registries(app)
        app.extensions["invenio-notifications"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("NOTIFICATIONS_"):
                app.config.setdefault(k, getattr(config, k))

    def init_manager(self, app):
        """Initialize manager."""
        manager = NotificationManager(
            backends=app.config["NOTIFICATIONS_BACKENDS"],
            builders=app.config["NOTIFICATIONS_BUILDERS"],
        )
        self.manager = manager

    def init_registries(self, app):
        """Initialize registries."""
        self.entity_resolvers = {
            er.type_key: er for er in app.config["NOTIFICATIONS_ENTITY_RESOLVERS"]
        }
        for ep in entry_points(group="invenio_notifications.entity_resolvers"):
            er_cls = ep.load()
            self.entity_resolvers.setdefault(er_cls.type_key, er_cls())


def finalize_app(app):
    """Finalize app."""
    if app.config["NOTIFICATIONS_SETTINGS_VIEW_FUNCTION"]:
        current_menu.submenu("settings.notifications").register(
            endpoint="invenio_notifications_settings.index",
            text=_(
                "%(icon)s Notifications",
                icon=LazyString(lambda: f'<i class="{current_theme_icons.bell}"></i>'),
            ),
            order=2,
        )

        current_menu.submenu("breadcrumbs.settings.notifications").register(
            endpoint="invenio_notifications_settings.index",
            text=_("Notifications"),
        )
