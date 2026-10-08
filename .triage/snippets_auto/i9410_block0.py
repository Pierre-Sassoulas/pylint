import typing

import marshmallow


class Base:
    data_schema_class: typing.Optional[
        typing.Union[typing.Type[marshmallow.Schema], marshmallow.Schema]
    ] = None  # Marshmallow schema class for responses

    def get_schema_instance(self) -> marshmallow.Schema:
        if self.data_schema_class is None:
            raise NotImplementedError()

        if isinstance(self.data_schema_class, marshmallow.Schema):
            return self.data_schema_class

        schema = self.data_schema_class()
        return schema


class DerivedOne(Base):

    data_schema_class = marshmallow.Schema()

    def test_me(self):
        schema = self.get_schema_instance()
        schema.dump({})


class DerivedTwo(Base):

    data_schema_class = marshmallow.Schema

    def tesst_me(self):
        schema = self.get_schema_instance()
        schema.dump({})
