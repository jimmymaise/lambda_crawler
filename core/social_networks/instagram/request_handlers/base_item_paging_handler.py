from abc import ABCMeta, abstractmethod
from http import HTTPStatus

import requests

from core.constants.base_instagram_constant import LambdaResponseConst, IGResponseConst
from core.social_networks.instagram.schemas.base_item_paging_response import ResponsePagingItemSchema
from core.utils.common import Common


class BaseItemPagingHandler(object, metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        self.resource_type = None
        self.res_key_path_to_item_list = None
        self.single_item_res_schema = None

    @abstractmethod
    def get_request_url(self, url_options):
        pass

    @staticmethod
    def make_request_api(url, request_options):
        response = requests.get(url=url, **request_options)
        status_code = response.status_code
        return response.json(), status_code

    def parse_item_list_by_response(self, request_res):
        resource_response_dict = Common.get_dict_data_by_path(request_res, self.res_key_path_to_item_list)
        items = [self.single_item_res_schema.load(item[IGResponseConst.NODE]) for item in
                 resource_response_dict[IGResponseConst.EDGES]]
        return items

    def get_next_cursor_by_response(self, request_res):
        resource_response_dict = Common.get_dict_data_by_path(request_res, self.res_key_path_to_item_list)
        page_info = resource_response_dict[IGResponseConst.PAGE_INFO]
        if page_info[IGResponseConst.HAS_NEXT_PAGE]:
            return page_info[IGResponseConst.END_CURSOR]

    @staticmethod
    def get_response_when_success(items, cursor):
        response = {LambdaResponseConst.STATUS_CODE: HTTPStatus.OK,
                    LambdaResponseConst.BODY: items,
                    LambdaResponseConst.CURSOR: cursor
                    }
        return ResponsePagingItemSchema().load(response)

    @staticmethod
    def get_response_when_fail(request_res):
        return {LambdaResponseConst.STATUS_CODE: request_res.status_code,
                LambdaResponseConst.MESSAGE: request_res.text
                }

    def do_paging_request(self, url_options, request_options):
        request_url = self.get_request_url(url_options)
        request_res, status_code = self.make_request_api(url=request_url, request_options=request_options)

        if status_code == HTTPStatus.OK:
            items = self.parse_item_list_by_response(request_res)
            cursor = self.get_next_cursor_by_response(request_res)
            return self.get_response_when_success(items, cursor)

        return self.get_response_when_fail(request_res)
