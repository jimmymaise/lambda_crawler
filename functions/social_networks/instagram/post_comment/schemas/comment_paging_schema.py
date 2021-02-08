from marshmallow import Schema, fields, EXCLUDE


class PagingCommentUrlOptionsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    cursor = fields.Str(allow_none=True)
    query_hash = fields.Str()
    num_item = fields.Int()
    shortcode = fields.Str()


class PagingCommentRequestOptionsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    cookies = fields.Dict()
    timeout = fields.Int()


class AccountInfoSchema(Schema):
    """Schema of account info"""
    class Meta:
        unknown = EXCLUDE

    info = fields.Dict(required=True, allow_none=False)
    account_if = fields.Str(required=True, allow_none=False)


class RequestSchema(Schema):
    """Schema of request param"""
    class Meta:
        unknown = EXCLUDE

    shortcode = fields.Str(required=True, allow_none=False)
    cursor = fields.Str(required=False, allow_none=True)
    num_item = fields.Int(required=False, allow_none=False)
    account_info = fields.Nested(AccountInfoSchema, required=True, allow_none=False)
