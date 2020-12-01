from marshmallow import Schema, fields


class ResponsePagingItemSchema(Schema):
    status_code = fields.Int()
    body = fields.List(fields.Dict)
    cursor = fields.Str(allow_none=True)
