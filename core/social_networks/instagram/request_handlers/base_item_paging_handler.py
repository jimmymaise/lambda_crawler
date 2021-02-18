from abc import ABCMeta, abstractmethod
from http import HTTPStatus

import requests

from core.constants.base_instagram_constant import LambdaResponseConst, IGResponseConst, DEFAULT_HEADER
from core.social_networks.instagram.schemas.base_item_paging_response import ResponsePagingItemSchema
from core.utils.common import Common


class BaseItemPagingHandler(object, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        self.resource_type = None
        self.res_key_path_to_item_list = None
        self.single_item_res_schema = None

    @staticmethod
    def make_request_api(url, request_options):
        response = requests.get(url=url, headers=DEFAULT_HEADER, **request_options)
        status_code = response.status_code
        return response.json(), status_code

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
