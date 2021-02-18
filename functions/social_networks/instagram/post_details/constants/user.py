"""
Include constant for:
    - Response of Lambda field
    - Response mapping from IG request
"""


class UserConst:
    """
    Constant for Response mapping - User from IG request with cookie
    """
    USER_ID = "id"
    USERNAME = "username"
    NUM_FOLLOWER = "edge_followed_by"
    FULL_NAME = "full_name"
    IS_VERIFY = "is_verified"
    NUM_PHOTO = "edge_owner_to_timeline_media"
    AVATAR = "profile_pic_url"


class ResponseFields:
    """
    Constant for Response fields - User
    (Base on "Data interface" in PRD - Lambda Function - IG Post Details)
    """
    USER_ID = "_id"
    USERNAME = "username"
    NUM_FOLLOWER = "num_follower"
    FULL_NAME = "full_name"
    IS_VERIFY = "is_verify"
    NUM_PHOTO = "num_photo"
    AVATAR = "avatar"
