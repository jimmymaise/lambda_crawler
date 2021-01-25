"""
Class for get Post details info
"""
class LoginRegexStr:
    "Regex var for Post with login"
    NUM_REACTION = r"subscription\_target\_id\:\"%d\".*reaction\_count\:\{count\:(\d+)\}"
    NUM_SHARE = r"subscription\_target\_id\:\"%d\".*share\_count\:\{count\:(\d+)\}"
    NUM_COMMENT = r'subscription\_target\_id\:\"%d\".*comment\_count.*count\:{total_count\:(\d+)'
    POST_ID = r"href\=\"https\:\/\/m\.facebook\.com\/\S+\/\w+\/(\d+).*\s\/\>\<link"
    CONTENT_TAG = "div"
    CONTENT_IDS = {"data-testid": "post_message"}
    POST_IMG = r'''class=\"do00u71z ni8dbmo4 stjgntxs l9j0dhe7\"\s .*
                \<div class\=\".*\" style\=\".*\"\>'
                \<img alt\=\"\" .* src\=\"(\S+)"\>'''
    VIEW_COUNT = r"interactioncount\:(\d+)"
    TIMESTAMP = r'\"story\"\:\S+\"creation\_time\"\:(\d+)'
    FEEDBACK_ID = r'feedback_id\"\:\"(\S+)\",\"viewer'


class NotLoginRegexStr:
    "Regex var for Post without login"
    NUM_REACTION = r"subscription\_target\_id\:\"%d\".*reaction\_count\:\{count\:(\d+)\}"
    NUM_SHARE = r"subscription\_target\_id\:\"%d\".*share\_count\:\{count\:(\d+)\}"
    NUM_COMMENT = r'subscription\_target\_id\:\"%d\".*comment\_count.*count\:{total_count\:(\d+)'
    POST_ID = r"href\=\"https\:\/\/m\.facebook\.com\/\S+\/\w+\/(\d+).*\s\/\>\<link"
    CONTENT_TAG = "div"
    CONTENT_IDS = {"data-testid": "post_message"}
    POST_IMG = r'meta property\=\"og\:image\" content\=\"(\S+)" \/\>\<meta property\=\"og\:url\"'
    VIEW_COUNT = r"interactioncount\:(\d+)"
    TIMESTAMP = r'abbr data\-utime\="(\d+)"'
    FEEDBACK_ID = r'feedbackSource:\d+\,feedbackTargetID\:"(\S+)"\,focusCommentID'


class ResponseFields:
    "Response constant fields for Post"
    POST_ID = "_id"
    NUM_REACTION = "num_reaction"
    NUM_COMMENT = "num_comment"
    NUM_SHARE = "num_share"
    POST_IMG = "full_picture"
    VIEW_COUNT = "view_count"
    TIMESTAMP = "taken_at_timestamp"
    FEEDBACK_ID = "feedback_id"
    CONTENT = "content"