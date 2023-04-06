from invenio_records_resources.references.registry import ResolverRegistryBase

from .proxies import current_notifications


class EntityResolverRegistry(ResolverRegistryBase):
    """Entity Resolver registry for notification context."""

    @classmethod
    def get_registered_resolvers(cls):
        """Get all currently registered resolvers."""
        return iter(current_notifications.entity_resolvers.values())
