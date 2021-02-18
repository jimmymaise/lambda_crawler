"""
Main file for collection service
"""
try:
    import unzip_requirements
except ImportError:
    pass
import traceback
from pathlib import Path

import core.constants.base_facebook_constant as fb_constant
from core.utils.exceptions import ErrorSocialType
from functions.social_networks.facebook.post_comment.config_logging.config_handler import Config
from functions.social_networks.facebook.post_comment.request_handlers.graph_api_handler import GraphApiHandler
from functions.social_networks.facebook.post_comment.request_handlers.graphql_api_handler import GraphQLHandler

function_path = str(Path(__file__).resolve().parents[1])


class MainStep:
    """Class for parsing post info"""

    def __init__(self, event, context):
        self.post_app_id = event.get('post_app_id')
        self.social_type = event.get('social_type')
        self.account_info = event.get('account_info')
        self.cursor = event.get('cursor')
        self.context = context
        self.config = Config.init_config(function_path=function_path)

    def crawl_post_details(self):
        """Crawl post details from post link"""
        response_const = fb_constant.LambdaResponseConst
        response_obj = response_const.RESPONSE_FORMAT

        # Check social type: If social type is invalid, raise Error and stop process
        if self.social_type not in fb_constant.LIST_USER_TYPE:
            raise ErrorSocialType("Social type is invalid")

        # Check 'post_app_id' type: If it it is invalid, raise Error and stop process
        if isinstance(self.post_app_id, str):
            collection_handler = GraphApiHandler(self.post_app_id, self.account_info) \
                if self.social_type == 'facebook_page' \
                else GraphQLHandler(self.post_app_id)
            list_comment, paging = collection_handler.get_comments(next_cursor=self.cursor)
            response_obj[response_const.DATA_FIELD] = list_comment
            response_obj[response_const.PAGING_FIELD] = paging
        else:
            raise TypeError("'post_app_id' is invalid")
        return response_obj


def lambda_handler(event, context):
    """Function handle request"""
    try:
        return MainStep(event, context).crawl_post_details()
    except Exception:
        raise RuntimeError(f"Error: {traceback.format_exc()}")


if __name__ == "__main__":
    test = {
        "post_app_id": "10209309845885030_1640100119495628",
        "social_type": "facebook_page",
        "account_info": None,
        "cursor": "AQHR4hZouMak-nbCLEsQHPL3lbqnQBo1RjGnsGNkmH_WcrHy_RLgwauYYB7XNB-ZO2tYkqY0XAQNi8y2givnq57EAw"
    }
    print(lambda_handler(test, None))
