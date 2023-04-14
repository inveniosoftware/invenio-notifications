from abc import ABC, abstractmethod
from typing import Dict

from invenio_notifications.models import Recipient


class RecipientFilter(ABC):
    """Recipient filter for a notification."""

    @abstractmethod
    def __call__(self, notification, recipients: Dict[str, Recipient]):
        """Filter recipients."""
        return recipients
