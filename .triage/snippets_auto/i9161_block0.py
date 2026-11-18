Pylint flags this usage:


    dataclasses.make_dataclass(
        cls_name="nombre",
        fields=[(id, int, dataclasses.field(default=None)) for id in fields],
    )
