# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 CERN.
# Copyright (C) 2023 Graz University of Technology.
# Copyright (C) 2026 TU Wien.
#
# Invenio-Notifications is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Base notification builder class, which builds and processes notifications.

As the name implies, notification builders take care of building ``Notification``
instances, via the ``build()`` function that needs to be implemented by subclasses.

The resulting ``Notification`` will then typically have a ``type`` property with
a value determined by the notification builder, and the other keyword arguments
would get put into the ``context`` property.

The notification can then be processed by the ``broadcast_notification()`` task, or
via the current ``NotificationManager`` directly.

The latter (which may run in a different Python interpreter, in case of the background
task) then resolves the ``NotificationBuilder`` to be used to handle the notification,
based on the ``type`` property and processes the event with it.

In the end, the notification builder will generate a list of ``NotificationBackend``
instances that are used to dispatch the notifications.

A very brief example, missing generators and filters for the builder:

.. code-block:: python

    from flask import g
    from invenio_notifications.models import Notification
    from invenio_notifications.services.builders import NotificationBuilder
    from invenio_notifications.tasks import broadcast_notification

    class MyNotificationBuilder(NotificationBuilder):
        type = "my-notification"

        # the builder's configuration for *processing* notifications
        # (left empty for brevity here; of course needs to be populated for actual use)
        context = []
        recipients = []
        recipient_filters = []
        recipient_backends = []

        # helper for *initially building* the notifications
        @classmethod
        def build(cls, identity=None, request=None, **kwargs):
            ctx = {"executing_id": identity, "request": request}
            return Notification(type=cls.type, context=ctx)

    notif = MyNotificationBuilder.build(identity=g.identity, request={"id": 1234})

    # send the notification to be handled in a background task
    # (this will require the right entries in ``app.config``)
    broadcast_notification.delay(notif.dumps())

"""

from abc import ABC, abstractmethod


class NotificationBuilder(ABC):
    """Base notification builder.

    Notification builders are used to both initially build ``Notification`` instances
    (via the ``build()`` method), as well as process/broadcast notifications (via the
    other methods).

    Subclasses are expected to provide overrides for the class variables, but can
    typically reuse the methods as is.
    """

    context = []
    """List of ``ContextGenerator`` to update notification context.

    The entries of this list are used to further populate and possibly override the
    (initially probably pretty bare-bones) ``notification.context``.

    Example: Initially, ``notification.context["request"]`` only holds the request ID.
    The first ``ContextGenerator`` resolves the referenced request and replaces
    ``notification.context["request"]`` with it.
    Further context generators then resolve the request's creator, receiver, etc.
    and replace the corresponding entries in the dictionary with the values (possibly
    also all dictionaries, but expanded with further information).
    """

    recipients = []
    """List of ``RecipientGenerator`` to generate a dictionary of unique recipients.

    The entries of this list are used to generate a dictionary of recipients with the
    recipients' IDs as keys and the corresponding ``Recipient`` instances as values
    from the notification (after the context was expanded).

    Example: Take the expanded references to relevant entities (creator, receiver, ...)
    from ``request.context`` and generate the recipients dictionary from it.
    """

    recipient_filters = []
    """List of ``RecipientFilter`` to filter the dictionary of recipients.

    The entries of this list are used to filter out some recipients from the
    recipients dictionary.

    Example: Filter out the user who is responsible for the notification, from the
    recipients dictionary.
    """

    recipient_backends = []
    """List of ``RecipientBackendGenerator`` to determine notification backends.

    The entries of this list are used to generate a list of backends that will
    be used to dispatch the notification.

    Example: Use email and chat backends to dispatch the notification to the
    collected and filtered recipients.
    """

    type = "Notification"
    """The notification type built by this builder.

    Typically, this will be used to tag the built notifications, and to resolve
    the "correct" notification builder to process/broadcast the notification later on.
    It may also be used to determine the Jinja template to render for the notification.
    """

    @classmethod
    @abstractmethod
    def build(cls, **kwargs):
        """Build notification based on type and additional context."""
        raise NotImplementedError()

    @classmethod
    def resolve_context(cls, notification):
        """Resolve all references in the notification context."""
        for ctx_func in cls.context:
            # NOTE: We assume that the notification is mutable and modified in-place
            ctx_func(notification)
        return notification

    @classmethod
    def build_recipients(cls, notification):
        """Return a dictionary of unique recipients for the notification."""
        recipients = {}
        for recipient_func in cls.recipients:
            recipient_func(notification, recipients)
        return recipients

    @classmethod
    def filter_recipients(cls, notification, recipients):
        """Apply filters to the recipients."""
        for recipient_filter_func in cls.recipient_filters:
            recipient_filter_func(notification, recipients)
        return recipients

    @classmethod
    def build_recipient_backends(cls, notification, recipient):
        """Return the notification backends for recipients."""
        backends = []
        for recipient_backend_func in cls.recipient_backends:
            recipient_backend_func(notification, recipient, backends)
        return backends
