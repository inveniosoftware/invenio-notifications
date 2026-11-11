# SPDX-FileCopyrightText: 2023 CERN.
# SPDX-FileCopyrightText: 2026 CESNET a.l.e.
# SPDX-License-Identifier: MIT

"""Pytest configuration.

See https://pytest-invenio.readthedocs.io/ for documentation on which test
fixtures are available.
"""

import pytest
from celery import Celery
from flask import Flask
from invenio_app.factory import create_app as _create_app
from invenio_i18n import InvenioI18N
from invenio_mail import InvenioMail
from jinja2 import DictLoader

from invenio_notifications import InvenioNotifications
from invenio_notifications.backends.email import EmailNotificationBackend
from invenio_notifications.models import Notification, Recipient
from invenio_notifications.services.builders import NotificationBuilder
from invenio_notifications.services.generators import (
    EmailBackendGenerator,
    RecipientGenerator,
)


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


class ContextEmailRecipient(RecipientGenerator):
    """Recipient generator extracting email from notification context."""

    def __init__(self, key="recipient_email"):
        """Initialize generator with context key."""
        self.key = key

    def __call__(self, notification, recipients):
        """Add recipient from notification context to recipients dictionary."""
        email = notification.context.get(self.key)
        if email:
            recipients[email] = Recipient(data={"email": email})
        return recipients


class ExampleNotificationBuilder(NotificationBuilder):
    """Concrete notification builder for tests."""

    type = "example_notification"
    recipients = [ContextEmailRecipient()]
    recipient_backends = [EmailBackendGenerator()]

    @classmethod
    def build(cls, recipient_email="recipient@example.org", **kwargs):
        """Build notification."""
        return Notification(
            type=cls.type,
            context={"recipient_email": recipient_email, **kwargs},
        )


@pytest.fixture
def example_builder():
    """Fixture providing ExampleNotificationBuilder."""
    return ExampleNotificationBuilder


@pytest.fixture
def notifications_app(example_builder):
    """Create a Flask app configured with Celery, InvenioMail, and InvenioNotifications."""
    app = Flask("testapp")
    app.config["MAIL_DEFAULT_SENDER"] = "noreply@example.org"
    app.config["MAIL_DEFAULT_REPLY_TO"] = "noreply@example.org"
    app.config["MAIL_SUPPRESS_SEND"] = True
    app.config["NOTIFICATIONS_BUILDERS"] = {example_builder.type: example_builder}
    app.config["NOTIFICATIONS_BACKENDS"] = {
        EmailNotificationBackend.id: EmailNotificationBackend()
    }

    template_content = (
        "{% block subject %}Test Subject{% endblock %}\n"
        "{% block html_body %}<p>Test Body</p>{% endblock %}\n"
        "{% block plain_body %}Test Body{% endblock %}\n"
    )
    app.jinja_loader = DictLoader(
        {
            f"invenio_notifications/{example_builder.type}.jinja": template_content,
            f"invenio_notifications/email/{example_builder.type}.jinja": template_content,
        }
    )

    InvenioI18N(app)
    InvenioMail(app)
    celery = Celery("testapp")
    celery.conf.task_always_eager = True  # forced to run synchronously
    InvenioNotifications(app)
    return app
