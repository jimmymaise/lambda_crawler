from core.social_networks.instagram.request_handlers.base_item_paging_handler import BaseItemPagingHandler
from functions.social_networks.instagram.post_comment.constants.comment import CommentConst
from functions.social_networks.instagram.post_comment.schemas.comment_paging_schema import \
    IGPostCommentResponseSchema


class CommentPagingHandler(BaseItemPagingHandler):
    def __init__(self):
        super().__init__()
        self.single_item_res_schema = IGPostCommentResponseSchema()
        self.res_key_path_to_item_list = CommentConst.COMMENT_DATA_RESPONSE_KEY_PATH
        self.comment_response_schema = IGPostCommentResponseSchema()

    def get_request_url(self, url_options):
        request_url = CommentConst.COMMENT_URL_NO_CURSOR.format(
            **url_options) if not url_options[CommentConst.CURSOR] else CommentConst.COMMENT_URL_WITH_CURSOR.format(
            **url_options)
        return request_url
