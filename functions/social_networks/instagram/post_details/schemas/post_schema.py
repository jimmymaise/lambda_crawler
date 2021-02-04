from marshmallow import Schema, fields, EXCLUDE


class AccountInfoSchema(Schema):
    info = fields.Dict(required=True)
    account_id = fields.Str(required=True)


class RequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    link = fields.Str(required=True, allow_none=False)
    account_info = fields.Nested(
        AccountInfoSchema,
        required=True,
        allow_none=False
    )

