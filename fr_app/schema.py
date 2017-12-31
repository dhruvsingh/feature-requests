from marshmallow import validate, Schema, fields
from .utils import validate_date_in_future


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(dump_only=True)


class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)


class ProductAreaSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)


class FeatureRequestSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=[validate.Length(min=6, max=255)]
    )
    description = fields.Str(required=True)
    client_priority = fields.Int(required=True)
    user_id = fields.Int(required=True, load_from="user")
    client_id = fields.Int(required=True, load_from="client")
    product_area_id = fields.Int(required=True, load_from="product_area")
    user = fields.Str(dump_only=True)
    client = fields.Str(dump_only=True)
    product_area = fields.Str(dump_only=True)
    target_date = fields.Date(
        required=True,
        validate=[validate_date_in_future],
        error_messages={
            'null': {
                'message': 'Date should be in the format YYYY-MM-DD',
                'code': 400
            },
            'validator_failed': {
                'message': 'Date should be in the format YYYY-MM-DD',
                'code': 400
            },
            'required': {
                'message': 'Target date is required in the format YYYY-MM-DD',
                'code': 400
            }
        }
    )
    created_on = fields.DateTime(dump_only=True)
    updated_on = fields.DateTime(dump_only=True)
