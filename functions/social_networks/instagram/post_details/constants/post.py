"""
Include constant for:
    - Response of Lambda field
    - Response mapping from IG request
"""


class PostConst:
    """
    Constant for Response mapping - Post from IG request with cookie
    """
    POST_ID = "id"
    POST_IMG = "display_url"
    POST_TYPE = "__typename"
    NUM_LIKE = "edge_media_preview_like"
    NUM_COMMENT = "edge_media_preview_comment"
    NUM_VIEW = "video_view_count"  # only for video
    IS_VIDEO = "is_video"
    CREATED_TIME = "taken_at_timestamp"
    CONTENT = "edge_media_to_caption"
    SHORTCODE = "shortcode"
    LOCATION = "location"


class ResponseFields:
    """
    Constant for Response fields - Post
    (Base on "Data interface" in PRD - Lambda Function - IG Post Details)
    """
    POST_ID = "_id"
    POST_IMG = "display_url"
    POST_TYPE = "post_type"
    NUM_LIKE = "num_like"
    NUM_COMMENT = "num_comment"
    NUM_VIEW = "video_view_count"     # only for video
    CREATED_TIME = "taken_at_timestamp"
    CONTENT = "content"
    USER_ID = "user_id"
    USERNAME = "username"
    SHORTCODE = "shortcode"
    LOCATION = "location"


DEFAULT_HEADER = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " +
                  "AppleWebKit/537.36 (KHTML, like Gecko) " +
                  "Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.344",
    "accept": "text/html,application/xhtml+xml,application/xml;" +
              "q=0.9,image/avif,image/webp,image/apng,*/*;" +
              "q=0.8,application/signed-exchange;v=b3;q=0.9"
}