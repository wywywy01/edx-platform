"""
Class that encapsulates version-rich identification of collected
block structures.
"""
from .block_structure import BlockStructureBlockData
from .transformer_registry import TransformerRegistry


class VersionIdentifier(object):
    """
    """
    def __init__(self, **kwargs):
        self.root_usage_key = kwargs.get('root_usage_key')

        self.data_version = kwargs.get('data_version')
        self.data_timestamp = kwargs.get('data_timestamp')

        self.transformers_schema_version = kwargs.get(
            'transformers_schema_version',
            TransformerRegistry.get_write_version_hash,
        )
        self.block_structure_schema_version = kwargs.get(
            'block_structure_schema_version',
            BlockStructureBlockData.VERSION,
        )

    def __unicode__(self):
        """
        Returns a concise deterministic string value
        representing the object and its values.
        """
        return u':'.join(
            unicode(field) +
            '@' +
            unicode(getattr(self, field, None))
            for field in sorted(vars(self))
        )
