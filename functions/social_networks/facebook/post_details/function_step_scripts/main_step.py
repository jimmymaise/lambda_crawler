"""
Main file for collection service
"""
from http import HTTPStatus

try:
    import unzip_requirements
except ImportError:
    pass
from pathlib import Path
from core.utils.exceptions import ErrorSocialType
import core.constants.base_facebook_constant as fb_constant
from functions.social_networks.facebook.post_details.config_logging.config_handler import Config
from functions.social_networks.facebook.post_details.request_handlers.post_handler import PostHandler

function_path = str(Path(__file__).resolve().parents[1])


class MainStep:
    "Class for parsing post info"

    def __init__(self, event, context):
        self.link = event.get('link')
        self.social_type = event.get('social_type')
        self.account_info = event.get('account_info')
        self.context = context
        self.config = Config.init_config(function_path=function_path)

    def crawl_post_details(self):
        "Crawl post details from post link"
        response_const = fb_constant.LambdaResponseConst
        response_obj = response_const.RESPONSE_FORMAT
        if self.social_type not in fb_constant.LIST_USER_TYPE:
            raise ErrorSocialType("Social type is invalid")
        if isinstance(self.link, str):
            account_info = self.account_info['data'] if self.account_info else {}
            response_data, status_code, details_status = PostHandler(self.link, account_info,
                                                                     self.social_type).get_post_details()
            response_obj[response_const.DATA_FIELD] = response_data
            response_obj[response_const.STATUS_CODE] = status_code
            response_obj[response_const.DETAILS] = details_status
        else:
            raise TypeError(HTTPStatus.NOT_FOUND.phrase)
        return response_obj


def lambda_handler(event, context):
    "Function handle request"
    return MainStep(event, context).crawl_post_details()


if __name__ == "__main__":
    test = {
        "link": "https://www.facebook.com/rhymastic/posts/10214553500191289",
        "type": "user",
        "cookie": None
    }
    print(lambda_handler(test, None))
