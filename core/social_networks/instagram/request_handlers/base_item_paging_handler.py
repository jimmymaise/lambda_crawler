from abc import ABCMeta, abstractmethod
from http import HTTPStatus
import requests
from core.utils.common import Common, update_account_status
from core.social_networks.instagram.schemas.base_item_paging_response import ResponsePagingItemSchema
from functions.social_networks.instagram.post_comment.constants.comment import CommentConst
from functions.social_networks.instagram.post_comment.schemas.comment_paging_schema import PostCommentSchema
from core.constants.base_instagram_constant import LambdaResponseConst, IGResponseConst, DEFAULT_HEADER,\
                                                    UserResponseConst, CmtResponseConst


class BaseItemPagingHandler(object, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        self.resource_type = None
        self.res_key_path_to_item_list = None
        self.single_item_res_schema = None
        self.list_comment = list()

    @abstractmethod
    def get_request_url(self, url_options):
        pass

    @staticmethod
    def make_request_api(url, request_options):
        response = requests.get(url=url, headers=DEFAULT_HEADER, **request_options)
        status_code = response.status_code
        return response.json(), status_code

    def parse_and_transform_item_list_by_response(self, request_res):
        """Parse + transform comment from response data"""
        resource_response_dict = Common.get_dict_data_by_path(request_res, self.res_key_path_to_item_list)
        items = [item[IGResponseConst.NODE] for item in resource_response_dict[IGResponseConst.EDGES]]
        for item in items:
            self._transfrom_response_comment(item)
        return self.list_comment

    def get_next_cursor_by_response(self, request_res):
        resource_response_dict = Common.get_dict_data_by_path(request_res, self.res_key_path_to_item_list)
        page_info = resource_response_dict[IGResponseConst.PAGE_INFO]
        return {
                IGResponseConst.HAS_NEXT_PAGE: page_info[IGResponseConst.HAS_NEXT_PAGE],
                IGResponseConst.CURSOR: page_info[IGResponseConst.END_CURSOR],
        }

    @staticmethod
    def get_response_when_success(items, cursor):
        response = {
            LambdaResponseConst.DATA_FIELD: items,
            LambdaResponseConst.PAGING_FIELD: cursor,
            LambdaResponseConst.MESS_FIELD: HTTPStatus.OK.phrase,
            LambdaResponseConst.DESC_FIELD: HTTPStatus.OK.phrase
        }
        return ResponsePagingItemSchema().load(response)

    def do_paging_request(self, url_options, request_options):
        request_url = self.get_request_url(url_options)
        request_res, status_code = self.make_request_api(url=request_url, request_options=request_options)
        update_account_status(
            social_network="INSTAGRAM",
            account_id=url_options.get('account_id'),
            status_code=status_code,
            message=HTTPStatus(status_code).phrase
        )
        if status_code == HTTPStatus.OK:
            items = self.parse_and_transform_item_list_by_response(request_res)
            cursor = self.get_next_cursor_by_response(request_res)
            return self.get_response_when_success(items, cursor)
        else:
            raise requests.RequestException(HTTPStatus(status_code).phrase)

    def _transfrom_response_comment(self, raw_data: dict, parent_id=None):
        """Transform comment before response to client"""
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
                UserResponseConst.IS_VERIFY: raw_data[CommentConst.COMMENTER_FIELD][CommentConst.COMMENTER_VERIFY],
                UserResponseConst.USERNAME: raw_data[CommentConst.COMMENTER_FIELD][CommentConst.COMMENTER],
            }
        }
        if raw_data.get(CommentConst.COMMENT_THREAD)\
          and raw_data[CommentConst.COMMENT_THREAD][CommentConst.NUM_COUNT] > 0:
            for reply in raw_data[CommentConst.COMMENT_THREAD][IGResponseConst.EDGES]:
                self._transfrom_response_comment(
                    raw_data=reply[IGResponseConst.NODE],
                    parent_id=int(raw_data[CommentConst.COMMENT_ID])
                )
        if isinstance(parent_id, int):
            response_data[LambdaResponseConst.CMT_FIELD][CmtResponseConst.PARENT_CMT_ID] = parent_id
        self.list_comment.append(PostCommentSchema().load(response_data))
