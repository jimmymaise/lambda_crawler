"""
Basic constant for Facebook
"""


class FBBaseURLConstant:
    """Basic constant for Facebook"""
    BASE_FACEBOOK_URL = 'https://www.facebook.com/{object_identity}'
    BASE_FACEBOOK_PROFILE_URL = 'https://www.facebook.com/{user_identity}'
    LOGIN_PARAM = r"LoginFormController"


class LambdaRequestConst:
    """Request constant for AWS Lambda function"""
    DATA_TYPE = 'type'
    ACCOUNT = 'account'
    TOKEN = 'token'
    LINK = 'link'
    COOKIE = 'cookie'


class LambdaResponseConst:
    """Response constant for AWS Lambda function"""
    RESPONSE_FORMAT = {
        "data": {},
        "message": "Done"
    }
    STATUS_CODE = "status"
    MESS_FIELD = "message"
    DESC_FIELD = "description"
    DATA_FIELD = "data"
    USER_FIELD = "user"
    PAGE_FIELD = "page"
    POST_FIELD = "post"
    PAGING_FIELD = "paging"


class PostInfo:
    """Class for post info"""
    NUM_REACTION = "num_reaction"
    NUM_COMMENT = "num_comment"
    NUM_SHARE = "num_share"
    VIEW_COUNT = "view_count"
    FEEDBACK_ID = "feedback_id"


class UserInfo:
    """Class for user info"""
    USER_ID = "_id"
    USERNAME = "username"
    AVATAR = "avatar"
    FULL_NAME = "full_name"
    NUM_FOLLOW = "num_follower"


class PageInfo:
    """Class for page info response"""
    USER_ID = "app_id"
    USERNAME = "username"
    AVATAR = "avatar"
    FULL_NAME = "full_name"
    NUM_FOLLOW = "num_follower"


class CookieStatus:
    """Status of cookie: Alive / Expired"""
    ALIVE = "Alive"
    EXPIRED = 'Expired'


DEFAULT_HEADER = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                  "AppleWebKit/537.36 (KHTML, like Gecko) " +
                  "Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"
}

# Tor config
URL_CHECK_IP = "http://icanhazip.com/"
TOR_SERVER = '34.209.176.134'
TOR_PASSWORD = "hiipasia"
TOR_CONTROL_PORT = 9051
TOR_DEFAULT_PORT = 9050

# Comment syntax 
COMMENT_SYNTAX = r"\<\!\-\-|\-\-\>"

# Login syntax of URL
LOGIN_URL_SYNTAX = "login/?next="

# HTML tag for check 'post not found'
LOGIN_NOT_FOUND_HTML_TAG = "img"
LOGIN_NOT_FOUND_HTML_ATTRIBUTE = {"src": "/images/comet/empty_states_icons/permissions/permissions_gray_wash.svg"}
NLOGIN_NOT_FOUND_HTML_TAG = "a"
NLOGIN_NOT_FOUND_HTML_ATTRIBUTE = {"href": "/r.php?r=101"}

ACCOUNT_BAN_CODE = 190
ACCOUNT_SUCCESS_CODE = 200

LIST_USER_TYPE = ['facebook', 'facebook_page']
