from marshmallow import fields, Schema, validate, validates_schema, ValidationError

class TestSchema(Schema):
    test_url = fields.Str(required=True, validate=validate.Length(max=1000))

    @validates_schema
    def validate_test_url(self, data, **kwargs):
        if data['test_url'] and not data['test_url'].startswith('https://test.example.com'):
            raise ValidationError('URL must start with {}'.format('https://test.example.com'))
