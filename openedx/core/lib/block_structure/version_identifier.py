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
        self.data_version_guid = kwargs.get('data_version_guid')
        self.data_time_stamp = kwargs.get('data_time_stamp')
        self.block_structure_class_version = kwargs.get(
            'block_structure_class_version',
            BlockStructureBlockData.VERSION,
        )
        self.transformers_version_hash = kwargs.get(
            'transformers_version_hash',
            TransformerRegistry.get_write_version_hash,
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
