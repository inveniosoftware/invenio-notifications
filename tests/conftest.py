# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from flask import Flask
from invenio_app.factory import create_app as _create_app


@pytest.fixture(scope="module")
def app_config(app_config):
    """Override pytest-invenio app_config fixture."""
    # TODO: Override any necessary config values for tests
    # app_config["NOTIFICATIONS_FOOBAR"] = "test"
    return app_config


@pytest.fixture(scope="module")
def create_app(instance_path):
    """Application factory fixture."""
    return _create_app


@pytest.fixture
def simple_app():
    """Create a minimal Flask app for email resolution tests."""
    app = Flask("testapp")
    app.config["MAIL_DEFAULT_SENDER"] = "noreply@example.org"
    app.config["MAIL_DEFAULT_REPLY_TO"] = "noreply@example.org"
    return app
