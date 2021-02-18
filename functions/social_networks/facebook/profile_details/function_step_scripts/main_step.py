"""
Main file for collection service
"""
from http import HTTPStatus

try:
    import unzip_requirements
except ImportError:
    pass
from pathlib import Path
import core.constants.base_facebook_constant as fb_constant
from functions.social_networks.facebook.post_details.config_logging.config_handler import Config
from functions.social_networks.facebook.post_details.request_handlers.profile_handler import ProfileHandler

function_path = str(Path(__file__).resolve().parents[1])


class MainStep:
    "Class for parsing profile info"

    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.config = Config.init_config(function_path=function_path)

    def crawl_post_details(self):
        "Crawl profile details from link"
        request_const = fb_constant.LambdaRequestConst
        response_const = fb_constant.LambdaResponseConst
        response_obj = response_const.RESPONSE_FORMAT
        response_data = response_const.COLLECTED_DATA
        status_code = HTTPStatus.NOT_FOUND.value
        if self.event.get(request_const.LINK):
            if isinstance(self.event[request_const.LINK], str):
                url = self.event[request_const.LINK]
                cookie = self.event.get(request_const.COOKIE)
                user_type = self.event.get(request_const.DATA_TYPE, "user")
                crawl_handler = ProfileHandler(url, cookie, user_type)
                response_data, details_status = crawl_handler.get_profile_details()
            else:
                details_status = {
                    response_const.STATUS_CODE: HTTPStatus.BAD_REQUEST.value,
                    response_const.DETAILS: HTTPStatus.BAD_REQUEST.description,
                    response_const.COOKIE_STT: fb_constant.CookieStatus.ALIVE
                }
        else:
            details_status = {
                response_const.STATUS_CODE: status_code,
                response_const.DETAILS: HTTPStatus(status_code).description,
                response_const.COOKIE_STT: fb_constant.CookieStatus.ALIVE
            }
        response_obj[response_const.DATA_FIELD] = response_data
        response_obj[response_const.STT_FIELD] = details_status
        return response_obj


def lambda_handler(event, context):
    "Function handle request"
    return MainStep(event, context).crawl_post_details()
