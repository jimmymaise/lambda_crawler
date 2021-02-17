import json
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
        base_url = "https://www.instagram.com/graphql/query/?query_hash=%s&variables=" % url_options['query_hash']
        request_url = base_url + '{"shortcode":"%s","first":%s,"after":%s}'\
                      % (url_options['shortcode'], url_options['num_item'], json.dumps(url_options['cursor']))
        return request_url
