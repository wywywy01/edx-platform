"""
Models used by the block structure framework.
"""

from django.db import models
from openedx.core.djangoapps.xmodule_django.models import UsageKeyField


class BlockStructure(models.Model):
    """

    """
    data_usage_key = UsageKeyField(
        u'Identifier of the data whose BlockStructure is created.',
        blank=False,
        max_length=255,
        db_index=True,
    )
    data_version = models.CharField(
        u'Version of the data.',
        blank=True,
        max_length=255,
    )
    data_timestamp = models.DateTimeField(
        u'Timestamp of when the data was edited.',
        blank=True,
        null=True,
    )

    transformers_schema_version = models.CharField(
        u'Representation of the schema version of the transformers used during collection.',
        blank=False,
        max_length=255,
    )
    block_structure_schema_version = models.CharField(
        u'Hash of transformers versions',
        blank=False,
        max_length=255,
    )
