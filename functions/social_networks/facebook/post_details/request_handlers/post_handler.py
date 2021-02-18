"""
Post handler for crawl user + post info from HTML
"""
import re
import socket
from http import HTTPStatus

import requests
import socks
from bs4 import BeautifulSoup
from core.handlers.crawl_account_handler import CrawlAccountHandler
from stem import Signal
from stem.control import Controller

import core.constants.base_facebook_constant as fb_constant
import functions.social_networks.facebook.post_details.constants.post as post_const_module
import functions.social_networks.facebook.post_details.constants.user as user_const_module
import functions.social_networks.facebook.post_details.constants.video as video_const_module
from core.constants.core_constant import CoreConst
from core.utils.exceptions import PostNotFoundError


class PostHandler:
    "Class for post collection with HTTP request"

    def __init__(self, post_url: str, account_info: dict, social_type):
        self.post_url = post_url
        self.account_info = account_info
        self.social_type = social_type

    def get_post_details(self):
        "Get details of post from HTML"
        headers = self.__generate_header_for_request()
        response_fields = fb_constant.LambdaResponseConst
        social_user_type = response_fields.USER_FIELD \
            if self.social_type == "facebook" \
            else response_fields.PAGE_FIELD

        # Parse post details via HTTP request
        response_data, response_code = self.__collect_post_html(headers)

        # Check cookie status
        cookie_status = self.__check_cookie_status(response_data)

        if self.__post_not_found(response_data, cookie_status):
            raise PostNotFoundError("Post can not access. Please check again")

        # Get basic info of owner
        profile_info = self.__parse_profile_info(response_data, cookie_status)

        # Get details info of post
        post_info = self.__parse_post_info(response_data, cookie_status)

        result = {
            social_user_type: profile_info,
            response_fields.POST_FIELD: post_info
        }
        return result, response_code, HTTPStatus(response_code).description

    def __check_cookie_status(self, response_data):
        "Check cookie status from HTML element and update account status"
        regex_str = fb_constant.FBBaseURLConstant.LOGIN_PARAM
        account_mananger = CrawlAccountHandler(
            account_base_url=CoreConst.AM_API,
            social_network='FACEBOOK',
            service_name='POST_REPORT',
            country=None
        )
        if response_data:
            login_element = re.findall(regex_str, response_data)
            cookie_status = False if login_element else True
        else:
            cookie_status = True

        # Update account status
        if self.account_info:
            account_mananger.update_account_token(
                account_id=self.account_info.get('account_id'),
                status_code=fb_constant.ACCOUNT_SUCCESS_CODE if cookie_status else fb_constant.ACCOUNT_BAN_CODE,
                message=fb_constant.CookieStatus.ALIVE if cookie_status else fb_constant.CookieStatus.EXPIRED
            )
        return cookie_status

    def __generate_header_for_request(self):
        "Generate header for FB request"
        header = fb_constant.DEFAULT_HEADER
        cookie_field_name = fb_constant.LambdaRequestConst.COOKIE
        if self.account_info.get('info'):
            header[cookie_field_name] = self.account_info['info']
        return header

    def __parse_profile_info(self, response_data: str, cookie_status: bool):
        """Get User/Page info base on cookie status"""
        response_const = fb_constant.UserInfo if self.social_type == 'facebook' \
            else fb_constant.PageInfo

        # Get regex str base on cookie status
        user_const = user_const_module.UserLoginRegexStr if cookie_status \
            else user_const_module.UserNLoginRegexStr

        # Get user info from response data
        list_username = re.findall(user_const.USERNAME, response_data)
        list_user_id = re.findall(user_const.USER_ID, response_data)
        list_user_avatar = re.findall(user_const.USER_AVATAR, response_data)
        list_full_name = re.findall(user_const.FULL_NAME, response_data)
        profile_info = {
            response_const.USERNAME: list_username[0] if list_username else "",
            response_const.USER_ID: int(list_user_id[0]) if list_user_id else 0,
            response_const.AVATAR: list_user_avatar[0].replace("amp;", "") if list_user_avatar else "",
            response_const.FULL_NAME: list_full_name[0] if list_full_name else "",
        }
        return profile_info

    def __parse_post_info(self, response_data: str, cookie_status: bool):
        """Get post info from HTML base on cookie status"""
        # Remove "comment" tag
        response_data = re.sub(fb_constant.COMMENT_SYNTAX, "", response_data)
        soup_obj = BeautifulSoup(response_data, 'html.parser')

        # Get regex str base on cookie status
        if "/videos/" in self.post_url:
            response_const = video_const_module.ResponseFields
            regex_module = video_const_module
        else:
            response_const = post_const_module.ResponseFields
            regex_module = post_const_module

        post_const = regex_module.LoginRegexStr if cookie_status \
            else regex_module.NotLoginRegexStr

        # Get post info from response data
        list_post_id = re.findall(post_const.POST_ID, response_data)
        post_id = int(list_post_id[0]) if list_post_id else None
        if not post_id:
            raise TypeError("Fail to get 'post ID'")

        list_num_reaction = re.findall(post_const.NUM_REACTION % post_id, response_data)
        list_num_comment = re.findall(post_const.NUM_COMMENT % post_id, response_data)
        list_num_share = re.findall(post_const.NUM_SHARE % post_id, response_data)
        list_num_view = re.findall(post_const.VIEW_COUNT, response_data)
        list_timestamp = re.findall(post_const.TIMESTAMP, response_data)
        list_post_img = re.findall(post_const.POST_IMG, response_data)

        content_obj = soup_obj.find(post_const.CONTENT_TAG, post_const.CONTENT_IDS)
        list_feedback = re.findall(post_const.FEEDBACK_ID, response_data)
        if list_feedback and "feedbackTargetID" in list_feedback[0]:
            list_feedback = re.findall(r"feedbackTargetID:\"(\S+)\"", list_feedback[0])
        # Remove empty element from list
        list_post_img = [img_url for img_url in list_post_img if img_url]
        post_info = {
            response_const.NUM_REACTION: int(list_num_reaction[0]) if list_num_reaction else 0,
            response_const.NUM_COMMENT: int(list_num_comment[0]) if list_num_comment else 0,
            response_const.NUM_SHARE: int(list_num_share[0]) if list_num_share else 0,
            response_const.VIEW_COUNT: int(list_num_view[0]) if list_num_view else 0,
            response_const.POST_ID: int(list_post_id[0]) if list_post_id else None,
            response_const.FEEDBACK_ID: list_feedback[0] if list_feedback else "",
            response_const.TIMESTAMP: int(list_timestamp[0]) if list_timestamp else None,
            response_const.POST_IMG: list_post_img[0].replace("amp;", "") if list_post_img else "",
            response_const.CONTENT: content_obj.text if content_obj else "",
        }
        return post_info

    def __collect_post_html(self, headers: dict):
        """Collect post details"""
        response_data, response_code, response_url = self.__collect_post_html_with_normal_method(headers)
        if fb_constant.LOGIN_URL_SYNTAX in response_url:
            response_data, response_code = self.__collect_post_html_with_socket_method(headers)
        return response_data, response_code

    def __collect_post_html_with_socket_method(self, headers: dict):
        """Collect post detail (HTML) via Tor server"""
        response_data = ""
        with Controller.from_port(fb_constant.TOR_SERVER, fb_constant.TOR_CONTROL_PORT) as controller:
            controller.authenticate(fb_constant.TOR_PASSWORD)
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, fb_constant.TOR_SERVER, fb_constant.TOR_DEFAULT_PORT)
            socket.socket = socks.socksocket
            response_obj = requests.get(url=self.post_url, headers=headers)
            while fb_constant.LOGIN_URL_SYNTAX in response_obj.url:
                controller.signal(Signal.NEWNYM)
                response_obj = requests.get(url=self.post_url, headers=headers)
        response_data = response_obj.text
        response_code = HTTPStatus.OK.value
        return response_data, response_code

    def __collect_post_html_with_normal_method(self, headers: dict):
        """Collect post detail (HTML) by AWS Lambda"""
        response_data = ""
        try:
            response_obj = requests.get(url=self.post_url, headers=headers)
        except requests.ConnectTimeout:
            response_code = HTTPStatus.REQUEST_TIMEOUT.value
        else:
            response_data = response_obj.text
            response_code = HTTPStatus.OK.value
            response_url = response_obj.url
        return response_data, response_code, response_url

    @classmethod
    def __post_not_found(cls, response_data, cookie_status):
        """Check post can access or not from HTML tag.
        If HTML tag have "not found" tag, return True, else return False"""
        soup = BeautifulSoup(response_data, 'html.parser')
        if cookie_status:
            html_tag = fb_constant.LOGIN_NOT_FOUND_HTML_TAG
            html_attr = fb_constant.LOGIN_NOT_FOUND_HTML_ATTRIBUTE
        else:
            html_tag = fb_constant.NLOGIN_NOT_FOUND_HTML_TAG
            html_attr = fb_constant.NLOGIN_NOT_FOUND_HTML_ATTRIBUTE
        login_tag = soup.find(html_tag, html_attr)
        return bool(login_tag)
