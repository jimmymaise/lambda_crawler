"""
Post handler for crawl "user" info from HTML
"""
import re
from http import HTTPStatus

import functions.social_networks.facebook.profile_details.constants.page as page_const_module
import functions.social_networks.facebook.profile_details.constants.user as user_const_module
import requests

import core.constants.base_facebook_constant as fb_constant


class ProfileHandler:
    "Class for post request"

    def __init__(self, post_url: str, cookies_str: str, user_type: str):
        self.post_url = post_url
        self.cookies_str = cookies_str
        self.user_type = user_type

    def get_profile_details(self):
        "Get details of profile from HTML"
        headers = self.__generate_header_for_request()
        response_fields = fb_constant.LambdaResponseConst
        cookie_const = fb_constant.CookieStatus
        response_data = ""
        try:
            response_obj = requests.get(url=self.post_url, headers=headers)
        except requests.ConnectTimeout:
            response_code = HTTPStatus.REQUEST_TIMEOUT.value
        except Exception:
            response_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
        else:
            response_data = response_obj.text
            response_code = HTTPStatus.OK.value
        finally:
            cookie_status = self.__check_cookie_status(response_data)
            cookie_details = cookie_const.ALIVE if cookie_status else cookie_const.EXPIRED
            profile_info = self.__parse_profile_info(response_data, cookie_status)
            result = {
                response_fields.USER_FIELD: profile_info,
            }
            details_status = {
                response_fields.STATUS_CODE: response_code,
                response_fields.DETAILS: HTTPStatus(response_code).description,
                response_fields.COOKIE_STT: cookie_details
            }
        return result, details_status

    @classmethod
    def __check_cookie_status(cls, response_data):
        "Check cookie status from HTML element"
        regex_str = fb_constant.FBBaseURLConstant.LOGIN_PARAM
        if response_data:
            login_element = re.findall(regex_str, response_data)
            cookie_status = False if login_element else True
        else:
            cookie_status = True
        return cookie_status

    def __generate_header_for_request(self):
        "Generate header for FB request"
        header = fb_constant.DEFAULT_HEADER
        cookie_field_name = fb_constant.LambdaRequestConst.COOKIE
        if self.cookies_str:
            header[cookie_field_name] = self.cookies_str
        return header

    def __parse_profile_info(self, response_data: str, cookie_status: bool):
        "Get User info base on cookie status and 'user type'"
        response_const = fb_constant.UserInfo
        profile_module = user_const_module if self.user_type == "user" else page_const_module
        profile_consts = profile_module.LoginRegexStr if cookie_status else profile_module.NotLoginRegexStr
        # Get user info from response data
        list_user_id = re.findall(profile_consts.USER_ID, response_data)
        list_username = re.findall(profile_consts.USERNAME, response_data)
        list_location = re.findall(profile_consts.LOCATION, response_data)
        list_full_name = re.findall(profile_consts.FULL_NAME, response_data)
        list_user_avatar = re.findall(profile_consts.AVATAR, response_data)
        list_num_follower = re.findall(profile_consts.NUM_FOLLOWER, response_data)
        profile_info = {
            response_const.USERNAME: list_username[0] if list_username else "",
            response_const.USER_ID: int(list_user_id[0]) if list_user_id else 0,
            response_const.AVATAR: list_user_avatar[0] if list_user_avatar else "",
            response_const.FULL_NAME: list_full_name[0] if list_full_name else "",
            response_const.LOCATION: list_location[0] if list_location else "",
            response_const.NUM_FOLLOW: int(list_num_follower[0]) if list_num_follower else 0,
        }
        return profile_info
