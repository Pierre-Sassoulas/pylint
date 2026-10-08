if not typing.TYPE_CHECKING:
    QuerySetBase = models.QuerySet
else:
    QuerySetBase = models.QuerySet[models.Model]
