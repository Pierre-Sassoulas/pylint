"""Repro attempt for the MRO RecursionError report.

The shape that recursed was a Django model whose base is chosen behind
``TYPE_CHECKING`` plus a ``methodtools`` cached method.
"""

from typing import TYPE_CHECKING

from django.db import models
from methodtools import lru_cache

if TYPE_CHECKING:
    _PipeDataRelatedMixinBase = models.Model
else:
    _PipeDataRelatedMixinBase = models.Model


class PipeDataRelatedMixin(_PipeDataRelatedMixinBase):
    class Meta:
        abstract = True

    @lru_cache()
    def cached(self):
        return 1
