# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio module for notifications support."""

from invenio_base.utils import load_or_import_from_config

from . import config
from .config import NOTIFICATIONS_CONFIG
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
        app.extensions["invenio-notifications"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("NOTIFICATIONS_"):
                app.config.setdefault(k, getattr(config, k))

    def init_manager(self, app):
        """Initialize manager."""
        cfg = load_or_import_from_config(
            "NOTIFICATIONS_CONFIG",
            app=app,
            default=NOTIFICATIONS_CONFIG,
        )
        manager = NotificationManager(
            config=cfg,
        )
        for backend_cls in cfg.backends:
            manager.register(backend_cls())

        self.manager = manager
