class CommentConst:
    CONST_CONFIG_FILE_PATH = 'config/config.json'
    COMMENT_DATA_RESPONSE_KEY_PATH = ['data', 'shortcode_media', 'edge_media_to_parent_comment']
    COMMENT_REPLY_RESPONSE_KEY_PATH = ['data', 'comment', 'edge_threaded_comments']
    COMMENT_RESOURCE_TYPE = 'COMMENT'
    REPLY_QUERY_HASH = "1ee91c32fc020d44158a3192eda98247"
    ACCOUNT = "account_info"
    ACCOUNT_ID = "account_id"
    COOKIE_FIELD = "info"
    NUM_ITEM = 'num_item'
    TIMEOUT = 'timeout'
    QUERY_HASH = 'query_hash'
    CURSOR = 'cursor'
    COOKIES = 'cookies'
    SHORTCODE = 'shortcode'
    NUM_COUNT = "count"
    # Comment
    COMMENT_ID = "id"
    COMMENT_MESS = "text"
    COMMENT_TIME = "created_at"
    COMMENT_LIKE = "edge_liked_by"
    COMMENT_THREAD = "edge_threaded_comments"
    # Commenter
    COMMENTER_FIELD = "owner"
    COMMENTER_ID = "id"
    COMMENTER = "username"
    COMMENTER_VERIFY = "is_verified"
    COMMENTER_AVATAR = "profile_pic_url"
