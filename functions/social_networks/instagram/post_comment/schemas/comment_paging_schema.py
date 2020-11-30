import time

from marshmallow import Schema, fields, pre_load, EXCLUDE

from core.constants.base_instagram_constant import LambdaRequestConst


class PagingCommentUrlOptionsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    cursor = fields.Str()
    query_hash = fields.Str()
    num_item = fields.Int()
    shortcode = fields.Str()


class PagingCommentRequestOptionsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    cookies = fields.Dict()
    timeout = fields.Int()


class IGPostCommentResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Integer()
    avatar = fields.Str()
    user_id = fields.Integer()
    username = fields.Str()
    message = fields.Str()
    take_at_timestamp = fields.Integer()

    @pre_load
    def process_response(self, data, **kwargs):
        data['take_at_timestamp'] = data.get('take_at_timestamp', data.get('created_at') or time.time())
        data['message'] = data.get('message', data.get('text'))
        data['_id'] = data.get('_id', data.get('id'))

        owner = data.get("owner")

        if owner:
            data.update(
                {
                    'avatar': owner.get('profile_pic_url'),
                    'username': owner.get('username'),
                    'user_id': owner.get('id')
                }
            )
        return data


class IGCommentPaginateRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    shortcode = fields.Str()
    cookies = fields.Dict()
    cursor = fields.Str(allow_none=True)
    num_item = fields.Int()
    query_hash = fields.Str()

    @pre_load
    def process_data_fields(self, data, **kwargs):
        data.update(data.get(LambdaRequestConst.DATA_FIELDS, {}))
        return data
