import json
from http import HTTPStatus

import requests

from core.constants.base_instagram_constant import LambdaResponseConst, IGResponseConst, UserResponseConst, \
    CmtResponseConst
from core.social_networks.instagram.request_handlers.base_item_paging_handler import BaseItemPagingHandler
from core.utils.common import Common, update_account_status
from functions.social_networks.instagram.post_comment.constants.comment import CommentConst
from functions.social_networks.instagram.post_comment.schemas.comment_paging_schema import IGPostCommentResponseSchema, \
    PostCommentSchema


class CommentPagingHandler(BaseItemPagingHandler):
    def __init__(self, url_options, request_options):
        super().__init__()
        self.single_item_res_schema = IGPostCommentResponseSchema()
        self.res_key_path_to_item_list = CommentConst.COMMENT_DATA_RESPONSE_KEY_PATH
        self.res_key_path_to_reply_list = CommentConst.COMMENT_REPLY_RESPONSE_KEY_PATH
        self.comment_response_schema = IGPostCommentResponseSchema()
        self.base_url = "https://www.instagram.com/graphql/query/?query_hash=%s&variables="
        self.list_comment = list()
        self.url_options = url_options
        self.request_options = request_options

    def get_request_url(self, url_options):
        """Generate URL to request and get comment"""
        request_url = self.base_url % url_options['query_hash'] + \
                      '{"shortcode":"%s","first":%s,"after":%s}' \
                      % (url_options['shortcode'], url_options['num_item'], json.dumps(url_options['cursor']))
        return request_url

    def get_request_url_for_reply(self, url_options):
        """Generate URL to request and get reply comment"""
        request_url = self.base_url % url_options.get('reply_query_hash', CommentConst.REPLY_QUERY_HASH) + \
                      '{"comment_id":"%s","first":%s,"after":%s}' \
                      % (url_options['comment_id'], url_options['num_item'], json.dumps(url_options['reply_cursor']))
        return request_url

    def do_paging_request(self):
        """Get list comment from IG post"""
        request_url = self.get_request_url(self.url_options)
        request_res, status_code = self.make_request_api(url=request_url, request_options=self.request_options)
        update_account_status(
            social_network="INSTAGRAM",
            account_id=self.url_options.get('account_id'),
            status_code=status_code,
            message=HTTPStatus(status_code).phrase
        )
        if status_code == HTTPStatus.OK:
            items = self.parse_and_transform_item_list_by_response(request_res)
            cursor = self.get_next_cursor_by_response(request_res)
            return self.get_response_when_success(items, cursor)
        else:
            raise requests.RequestException(HTTPStatus(status_code).phrase)

    def parse_and_transform_item_list_by_response(self, request_res: dict):
        """
        Parse + transform comment from response data
        Input:
        - request_res (dict): Response data after request into IG success
        Output:
        - list_comment (list): List comment + commenter info after parse and transform
        """
        resource_response_dict = Common.get_dict_data_by_path(request_res, self.res_key_path_to_item_list)
        items = [item[IGResponseConst.NODE] for item in resource_response_dict[IGResponseConst.EDGES]]
        for item in items:
            self._transfrom_response_comment(item)
        return self.list_comment

    def _transfrom_response_comment(self, raw_data: dict, parent_id=None):
        """
        Transform comment before response to client.
        Input:
        - raw_data (dict): Response data before parse and transform from IG
        - parent_id (int): Parent comment ID if have
        Output:
        - response_data (dict): Comment after parse and transform
        """
        response_data = {
            LambdaResponseConst.CMT_FIELD: {
                CmtResponseConst.MESSAGE: raw_data[CommentConst.COMMENT_MESS],
                CmtResponseConst.CREATED_AT: raw_data[CommentConst.COMMENT_TIME],
                CmtResponseConst.COMMENT_ID: int(raw_data[CommentConst.COMMENT_ID]),
                CmtResponseConst.NUM_LIKE: raw_data[CommentConst.COMMENT_LIKE][CommentConst.NUM_COUNT],
                CmtResponseConst.COMMENTER: raw_data[CommentConst.COMMENTER_FIELD][CommentConst.COMMENTER],
                CmtResponseConst.COMMENTER_ID: int(raw_data[CommentConst.COMMENTER_FIELD][CommentConst.COMMENTER_ID])
            },
            LambdaResponseConst.USER_FIELD: {
                UserResponseConst.USER_ID: int(raw_data[CommentConst.COMMENTER_FIELD][CommentConst.COMMENTER_ID]),
                UserResponseConst.AVATAR: raw_data[CommentConst.COMMENTER_FIELD][CommentConst.COMMENTER_AVATAR],
                UserResponseConst.IS_VERIFY: raw_data[CommentConst.COMMENTER_FIELD].get(CommentConst.COMMENTER_VERIFY,
                                                                                        False),
                UserResponseConst.USERNAME: raw_data[CommentConst.COMMENTER_FIELD][CommentConst.COMMENTER],
            }
        }
        if raw_data.get(CommentConst.COMMENT_THREAD):
            if raw_data[CommentConst.COMMENT_THREAD][CommentConst.NUM_COUNT] <= 3:
                for reply in raw_data[CommentConst.COMMENT_THREAD][IGResponseConst.EDGES]:
                    self._transfrom_response_comment(
                        raw_data=reply[IGResponseConst.NODE],
                        parent_id=int(raw_data[CommentConst.COMMENT_ID])
                    )
            else:
                self.url_options['reply_cursor'] = raw_data[CommentConst.COMMENT_THREAD][IGResponseConst.PAGE_INFO] \
                    .get(IGResponseConst.END_CURSOR)
                self._get_reply_comment(parent_id=int(raw_data[CommentConst.COMMENT_ID]))
        if isinstance(parent_id, int):
            response_data[LambdaResponseConst.CMT_FIELD][CmtResponseConst.PARENT_CMT_ID] = parent_id
        self.list_comment.append(PostCommentSchema().load(response_data))

    def _get_reply_comment(self, parent_id: int):
        """Get reply comment from parent comment ID
        Input:
        - parent_id (int): Parent comment ID need to get reply
        Output: Reply comment have been parse, transform and "append" into "self.list_comment"
        """
        self.url_options['comment_id'] = parent_id
        request_url = self.get_request_url_for_reply(self.url_options)
        request_res, status_code = self.make_request_api(url=request_url, request_options=self.request_options)
        if status_code == HTTPStatus.OK:
            resource_response_dict = Common.get_dict_data_by_path(request_res, self.res_key_path_to_reply_list)
            for reply_cmt in resource_response_dict[IGResponseConst.EDGES]:
                self._transfrom_response_comment(reply_cmt[IGResponseConst.NODE], parent_id)
