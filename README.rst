..
    Copyright (C) 2023 CERN.
    Copyright (C) 2026 TU Wien.

    Invenio-Notifications is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

=======================
 Invenio-Notifications
=======================

.. image:: https://github.com/inveniosoftware/invenio-notifications/workflows/CI/badge.svg
        :target: https://github.com/inveniosoftware/invenio-notifications/actions?query=workflow%3ACI

.. image:: https://img.shields.io/github/tag/inveniosoftware/invenio-notifications.svg
        :target: https://github.com/inveniosoftware/invenio-notifications/releases

.. image:: https://img.shields.io/pypi/dm/invenio-notifications.svg
        :target: https://pypi.python.org/pypi/invenio-notifications

.. image:: https://img.shields.io/github/license/inveniosoftware/invenio-notifications.svg
        :target: https://github.com/inveniosoftware/invenio-notifications/blob/master/LICENSE

Invenio module for generic notifications support.
It can be used to send notifications via various backends (like email or chat, if implemented) to recipients (like users or groups).


Overview
========

The two main customizable components provided by ``Invenio-Notifications`` for controlling notifications are: ``NotificationBuilder`` and ``NotificationBackend``.

A ``NotificationBuilder`` is used to both initially build a ``Notification`` object with some context, as well as later on to process this notification to determine the recipients and backend to use for actually sending off the notification.

A ``NotificationBackend`` receives the notification data and its recipient, and takes care of rendering the notification and actually sending it off.

Another customizable component is the ``EntityResolver`` which is used to resolve entities that are referenced in a notification's serialized data
For instance, an ``EntityResolver`` would be used to find the user referenced by the dictionary ``{"user": "1"}`` and expand the notification's data with further information like the user's email address.
However, for most cases the provided defaults should be sufficient here.



Configuration
-------------

For ``Invenio-Notifications`` to do its job properly, the following configuration needs to be set (e.g. in ``invenio.cfg``):

.. code-block:: python

    from invenio_notifications.backends.email import EmailNotificationBackend
    from invenio_records_resources.references.entity_resolvers import ServiceResultResolver
    from my_package import MyNotificationBuilder

    # the notification builders need to be registered by their type as key, for the
    # notification manager (possibly in a background task running in another Python
    # interpreter) to look up the right notification builder for processing
    NOTIFICATIONS_BUILDERS = {
        MyNotificationBuilder.type: MyNotificationBuilder,
        # ...
    }

    # notification backends, responsible for actually sending out notifications
    NOTIFICATIONS_BACKENDS = {"email": EmailNotificationBackend}

    # entity resolvers, used for finding referenced entities like users in the built
    # notifications' data
    NOTIFICATIONS_ENTITY_RESOLVERS = [
        ServiceResultResolver(service_id="users", type_key="user"),
        ServiceResultResolver(service_id="groups", type_key="group"),
        # ...
    ]


Example
-------

Here is an annotated example for a ``NotificationBuilder`` used as part of a custom request type's "accept" action:

.. code-block:: python

    from invenio_notifications.models import Notification
    from invenio_notifications.registry import EntityResolverRegistry
    from invenio_notifications.services.builders import NotificationBuilder
    from invenio_notifications.services.generators import EmailBackendGenerator, EntityResolverContextGenerator
    from invenio_users_resources.notifications.filters import UserPreferencesRecipientFilter
    from invenio_users_resources.notifications.generators import UserRecipient

    class MyRequestNotificationBuilder(NotificationBuilder):
        """Base notification builder for "accept" events on my custom request type."""

        type = "my-request-type.accept"

        @classmethod
        def build(cls, request, result):
            """Build notification with request context."""
            return Notification(
                type=cls.type,

                # the context is used for determining the recipients, and is also
                # available for rendering the notification template
                context={
                    "request": EntityResolverRegistry.reference_entity(request),
                    "result": result,
                },
            )

        # first resolve the referenced request and expand the `notification.context` data;
        # afterwards expand the referenced creator, topic, and receiver
        context = [
            EntityResolverContextGenerator(key="request"),
            EntityResolverContextGenerator(key="request.created_by"),
            EntityResolverContextGenerator(key="request.topic"),
            EntityResolverContextGenerator(key="request.receiver"),
        ]

        # create a `Recipient` instance from the resolved request creator
        # (the other expanded entities may be relevant in template rendering)
        recipients = [
            UserRecipient(key="request.created_by"),
        ]

        # filter out recipients that have notifications disabled
        recipient_filters = [
            UserPreferencesRecipientFilter(),
        ]

        # use the email backend, which will render e.g. "my-request-type.accept.jinja"
        recipient_backends = [
            EmailBackendGenerator(),
        ]

    # ...
    # the builder needs to be registered in the `NOTIFICATIONS_BUILDERS` config;
    # here's how the builder would be typically used in request actions:
    # ...

    import random
    from invenio_requests.customizations.actions import AcceptAction
    from invenio_notifications.services.uow import NotificationOp

    class MyRequestTypeAcceptAction(AcceptAction):
        """Accept action for my custom request type, sending a notification."""

        def execute(self, identity, uow):
            """Calculate an important result on "accept" and send a notification."""
            result = random.randint(0, 100)
            uow.register(
                NotificationOp(
                    MyRequestNotificationBuilder.build(
                        request=self.request,
                        result=result,
                    )
                )
            )
            super().execute(identity, uow)

    # ...
    # further code for the customized request type and its registration is omitted
    # ...



Usage in the Invenio ecosystem
==============================

This package is used heavily in `Invenio-Requests <https://github.com/inveniosoftware/invenio-requests>`__ (or rather in the packages that implement requests) to send notifications to involved users whenever something happens with a request.

Generally, each request action generates a ``Notification`` via a dedicated ``NotificationBuilder`` and registers it to the action's ``UnitOfWork`` via a ``NotificationOp``.
Upon successful completion of the transaction, that will schedule a background task where the ``NotificationManager`` processes the notification.
Since the background task runs in another Python interpreter, the manager needs to look up the appropriate ``NotificationBuilder`` to use for processing the notification via the ``notification.type``.
The builder is then used to evaluate the recipients of the notification and the backend (like email) to use to finally render and send the notifications.

Concrete implementations of notification builders for various request actions can be found in `Invenio-RDM-Records <https://github.com/inveniosoftware/invenio-rdm-records>`__.
