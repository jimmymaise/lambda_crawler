from marshmallow import Schema, fields, EXCLUDE


class PagingCommentUrlOptionsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    cursor = fields.Str(allow_none=True)
    num_item = fields.Int()
    query_hash = fields.Str(required=True, allow_none=False)
    shortcode = fields.Str()
    account_id = fields.Str(required=True, allow_none=False)


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
    account_id = fields.Str(required=True, allow_none=False)
    query_hash = fields.Str(required=True, allow_none=False)


class IGCommentPaginateRequestSchema(Schema):
    """Schema of request param"""
    class Meta:
        unknown = EXCLUDE

    shortcode = fields.Str(required=True, allow_none=False)
    cursor = fields.Str(required=False, allow_none=True)
    num_item = fields.Int(required=False, allow_none=False)
    account_info = fields.Nested(AccountInfoSchema, required=True, allow_none=False)


class CommentResponseSchema(Schema):
    """Schema of comment param"""
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int(required=True, allow_none=False)
    message = fields.Str(required=True, allow_none=True)
    user_id = fields.Int(required=True, allow_none=False)
    username = fields.Str(required=False, allow_none=True)
    num_like = fields.Int(required=False, allow_none=True)
    parent_comment_id = fields.Int(required=False, allow_none=True)
    taken_at_timestamp = fields.Int(required=True, allow_none=False)


class UserResponseSchema(Schema):
    """Schema of user param"""
    class Meta:
        unknown = EXCLUDE

    _id = fields.Int(required=True, allow_none=False)
    username = fields.Str(required=True, allow_none=False)
    avatar = fields.Str(required=True, allow_none=False)
    is_verify = fields.Boolean(required=True, allow_none=False)


class PostCommentSchema(Schema):
    """Schema for post comment response"""
    class Meta:
        unknown = EXCLUDE

    user = fields.Nested(UserResponseSchema, required=True)
    comment = fields.Nested(CommentResponseSchema, required=True)


class IGPostCommentResponseSchema(Schema):
    """Schema of response data to API Gateway"""
    class Meta:
        unknown = EXCLUDE

    data = fields.Nested(PostCommentSchema, required=False)
    paging = fields.Dict()
    message = fields.Str()
    description = fields.Str()
