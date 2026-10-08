# pylint: disable=missing-module-docstring,missing-class-docstring
import typing

from django.db import models

if typing.TYPE_CHECKING:
    QuerySetBase = models.QuerySet[models.Model]
else:
    QuerySetBase = models.QuerySet


# class def will trigger: E0239: Inheriting 'QuerySetBase', which is not a class. (inherit-non-class)
class TestQuerySet(QuerySetBase):  
    pass
