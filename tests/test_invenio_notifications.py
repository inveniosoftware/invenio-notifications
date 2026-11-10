# SPDX-FileCopyrightText: 2023 CERN.
# SPDX-License-Identifier: MIT

"""Module tests."""

from unittest.mock import MagicMock, patch

from flask import Flask

from invenio_notifications import InvenioNotifications
from invenio_notifications.backends.email import EmailNotificationBackend
from invenio_notifications.manager import NotificationManager
from invenio_notifications.models import Notification, Recipient


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


class TestNotificationManagerBroadcast:
    """Test NotificationManager.broadcast method."""

    def test_broadcast_default_delay(self):
        """Test broadcast calls task.delay by default."""
        manager = NotificationManager(backends={}, builders={})
        notification = Notification(type="test_event", context={"key": "value"})

        with patch("invenio_notifications.manager.broadcast_notification") as mock_task:
            mock_sig = MagicMock()
            mock_task.si.return_value = mock_sig

            result = manager.broadcast(notification)

            mock_task.si.assert_called_once_with(
                {"type": "test_event", "context": {"key": "value"}}
            )
            mock_sig.delay.assert_called_once_with()
            mock_sig.apply.assert_not_called()
            assert result == mock_sig.delay.return_value

    def test_broadcast_eager(self):
        """Test broadcast calls task.apply when eager=True."""
        manager = NotificationManager(backends={}, builders={})
        notification = Notification(type="test_event", context={"key": "value"})

        with patch("invenio_notifications.manager.broadcast_notification") as mock_task:
            mock_sig = MagicMock()
            mock_task.si.return_value = mock_sig

            result = manager.broadcast(notification, eager=True)

            mock_task.si.assert_called_once_with(
                {"type": "test_event", "context": {"key": "value"}}
            )
            mock_sig.apply.assert_called_once_with()
            mock_sig.delay.assert_not_called()
            assert result == mock_sig.apply.return_value


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

    def test_resolve_email_group_without_domain(self, simple_app, caplog):
        """Test group name without domain config returns None and logs a warning."""
        with simple_app.app_context():
            simple_app.config["NOTIFICATIONS_GROUP_EMAIL_DOMAIN"] = None
            backend = EmailNotificationBackend()
            recipient = Recipient(data={"name": "physics-team"})
            email = backend._resolve_email(recipient)
            assert email is None
            assert "NOTIFICATIONS_GROUP_EMAIL_DOMAIN" in caplog.text

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
