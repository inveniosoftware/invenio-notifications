from abc import ABC, abstractmethod
from typing import Dict

from invenio_records.dictutils import dict_lookup, dict_set

from invenio_notifications.models import Notification, Recipient
from invenio_notifications.registry import EntityResolverRegistry


class ContextGenerator:
    """Payload generator for a notification."""

    @abstractmethod
    def __call__(self, notification: Notification):
        """Update notification context."""
        return notification


class RecipientGenerator(ABC):
    """Recipient generator for a notification."""

    @abstractmethod
    def __call__(self, notification, recipients: Dict[str, Recipient]):
        """Add recipients."""
        return recipients


class RecipientBackendGenerator(ABC):
    """Backend generator for a notification."""

    @abstractmethod
    def __call__(self, notification, recipient: Recipient, backends: list[str]):
        """Update required recipient information and add backend id."""
        return backends


class EntityResolve(ContextGenerator):
    def __init__(self, key):
        self.key = key

    def __call__(self, notification: Notification):
        """Update required recipient information and add backend id."""
        entity_ref = dict_lookup(notification.context, self.key)
        entity = EntityResolverRegistry.resolve_entity(entity_ref)
        dict_set(notification.context, self.key, entity)
        return notification
