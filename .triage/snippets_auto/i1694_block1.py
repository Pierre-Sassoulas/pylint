from collections import OrderedDict

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.inspection import inspect

Base = declarative_base()

class Model(Base):
    __abstract__ = True

    def __init__(self, **kwargs):
        super(Model, self).__init__()
        self.set_attrs(**kwargs)

    def set_attrs(self, **attrs):
        for attr_name, attr_value in attrs.items():
            if attr_name in self.fields:
                setattr(self, attr_name, attr_value)

    def to_dict(self):
        result = {}
        for attr_name in self.fields:
            attr_value = getattr(self, attr_name)
            if attr_value is not None:
                result[attr_name] = attr_value
        return result

    @declared_attr
    def __tablename__(cls):
        # pylint: disable=no-self-argument
        return plural(decapitalize(cls.__name__))

    @classproperty
    def columns(cls):
        columns = inspect(cls).mapper.column_attrs
        columns = list(sorted(columns, key=lambda column: column.key))
        return columns

    @classproperty
    def fields(cls):
        fields = OrderedDict([(column.key, getattr(cls, column.key))
                              for column in cls.columns])
        return fields

    @classproperty
    def primary_key_columns(cls):
        columns = list(inspect(cls).mapper.primary_key)
        return columns

    @classproperty
    def primary_key_fields(cls):
        fields = OrderedDict([(column.key, getattr(cls, column.key))
                              for column in cls.primary_key_columns])
        return fields

