# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2023 Graz University of Technology.
#
# Invenio-Notifications is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Proxies for accessing the currently instantiated notifications extension."""

from flask import current_app
from werkzeug.local import LocalProxy

current_notifications = LocalProxy(
    lambda: current_app.extensions["invenio-notifications"]
)
"""Proxy for the instantiated notifications extension."""

current_notifications_manager = LocalProxy(lambda: current_notifications.manager)
"""Proxy for the instantiated notifications manager."""
