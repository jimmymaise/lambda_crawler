from marshmallow import Schema, fields


class ResponsePagingItemSchema(Schema):
    data = fields.List(fields.Dict, allow_none=True)
    paging = fields.Dict(allow_none=True)
    message = fields.Str(required=True, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
