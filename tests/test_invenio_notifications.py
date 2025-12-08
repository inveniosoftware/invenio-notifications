# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

from flask import Flask

from invenio_notifications import InvenioNotifications
from invenio_notifications.backends.email import EmailNotificationBackend
from invenio_notifications.models import Recipient


def test_version():
    """Test version import."""
    from invenio_notifications import __version__

    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioNotifications(app)
    assert "invenio-notifications" in app.extensions

    app = Flask("testapp")
    ext = InvenioNotifications()
    assert "invenio-notifications" not in app.extensions
    ext.init_app(app)
    assert "invenio-notifications" in app.extensions


class TestEmailResolution:
    """Test email resolution logic for groups and users."""

    def test_resolve_email_with_explicit_email(self, simple_app):
        """Test that explicit email field takes precedence."""
        with simple_app.app_context():
            backend = EmailNotificationBackend()
            recipient = Recipient(
                data={"email": "user@example.org", "name": "testgroup"}
            )
            email = backend._resolve_email(recipient)
            assert email == "user@example.org"

    def test_resolve_email_with_email_hidden(self, simple_app):
        """Test email_hidden fallback."""
        with simple_app.app_context():
            backend = EmailNotificationBackend()
            recipient = Recipient(
                data={"email_hidden": "hidden@example.org", "name": "testgroup"}
            )
            email = backend._resolve_email(recipient)
            assert email == "hidden@example.org"

    def test_resolve_email_group_with_domain(self, simple_app):
        """Test group name formatting with domain."""
        with simple_app.app_context():
            simple_app.config["NOTIFICATIONS_GROUP_EMAIL_DOMAIN"] = "cern.ch"
            backend = EmailNotificationBackend()
            recipient = Recipient(data={"name": "physics-team"})
            email = backend._resolve_email(recipient)
            assert email == "physics-team@cern.ch"

    def test_resolve_email_group_without_domain(self, simple_app):
        """Test group name without domain config (backward compatible)."""
        with simple_app.app_context():
            simple_app.config["NOTIFICATIONS_GROUP_EMAIL_DOMAIN"] = None
            backend = EmailNotificationBackend()
            recipient = Recipient(data={"name": "physics-team"})
            email = backend._resolve_email(recipient)
            assert email == "physics-team"

    def test_resolve_email_name_with_at_symbol(self, simple_app):
        """Test name that already contains @ is used as-is."""
        with simple_app.app_context():
            simple_app.config["NOTIFICATIONS_GROUP_EMAIL_DOMAIN"] = "cern.ch"
            backend = EmailNotificationBackend()
            recipient = Recipient(data={"name": "team@external.org"})
            email = backend._resolve_email(recipient)
            assert email == "team@external.org"

    def test_resolve_email_no_email_no_name(self, simple_app):
        """Test missing email and name returns None."""
        with simple_app.app_context():
            backend = EmailNotificationBackend()
            recipient = Recipient(data={"id": "123"})
            email = backend._resolve_email(recipient)
            assert email is None

    def test_send_with_none_email_logs_warning(self, simple_app, caplog):
        """Test that None email logs warning and returns None."""
        with simple_app.app_context():
            backend = EmailNotificationBackend()
            recipient = Recipient(data={"id": "123"})
            notification = type("obj", (object,), {"type": "test-notification"})()

            result = backend.send(notification, recipient)

            assert result is None
            assert "Cannot send email notification" in caplog.text
