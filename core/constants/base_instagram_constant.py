# BASE URLs
class IGBaseURLConstant:
    BASE_INSTAGRAM_PAGING_URL = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables='
    BASE_INSTAGRAM_GET_ONE_ITEM_DETAIL_URL = 'https://www.instagram.com/{item_id}/?__a=1'


# Lambda Request
class LambdaRequestConst:
    DATA_FIELDS = 'data_fields'


# IG Request
class IGResponseConst:
    HAS_NEXT_PAGE = 'has_next_page'
    END_CURSOR = 'end_cursor'
    PAGE_INFO = 'page_info'
    NODE = 'node'
    EDGES = 'edges'
    STATUS_CODE = 'status_code'
    CURSOR = "cursor"


class LambdaResponseConst:
    """Response constant for AWS Lambda function"""
    RESPONSE_FORMAT = {
        "data": {},
        "message": "Done"
    }
    MESS_FIELD = "message"
    DESC_FIELD = "description"
    DATA_FIELD = "data"
    USER_FIELD = "user"
    POST_FIELD = "post"
    PAGING_FIELD = "paging"
    CMT_FIELD = "comment"


class UserResponseConst:
    """Response constant for user info"""
    USER_ID = "_id"
    USERNAME = "username"
    FULL_NAME = "full_name"
    IS_VERIFY = "is_verify"
    AVATAR = "avatar"
    NUM_FOLLOWER = "num_follower"
    NUM_FOLLOWING = "num_following"
    NUM_PHOTO = "num_photo"


class CmtResponseConst:
    """Response constant for commnet info"""
    COMMENT_ID = "_id"
    COMMENTER_ID = "user_id"
    COMMENTER = "username"
    CREATED_AT = "taken_at_timestamp"
    MESSAGE = "message"
    NUM_LIKE = "num_like"
    PARENT_CMT_ID = "parent_comment_id"  # If comment is "reply"
    POST_ID = "post_id"


DEFAULT_HEADER = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                  "AppleWebKit/537.36 (KHTML, like Gecko) " +
                  "Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"
}
