import typing

from marshmallow import fields
from marshmallow import validate


class AdminCancelOrders:
    order_ids: typing.List[int] = fields.List(fields.Int(), required=True, validate=validate.Length(min=1))

    def validate(self):
        pass
