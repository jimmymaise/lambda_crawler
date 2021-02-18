import json
import re
import socket
import time
from datetime import datetime

import requests
import socks
from requests_toolbelt.multipart.encoder import MultipartEncoder
from stem import Signal
from stem.control import Controller

import core.constants.base_facebook_constant as fb_const
import functions.social_networks.facebook.post_comment.constants.comment as cmt_const
from core.utils.exceptions import ErrorRequestFormat


class GraphQLHandler:
    """Class for comment collection via FB GraphQL API"""

    def __init__(self, post_app_id: str, **kwargs):
        self.post_id = self._get_post_id(post_app_id)
        self.list_comment = []
        self.counter = 0
        self.cursor = {'has_next_page': False, 'next_cursor': None}

    @classmethod
    def _get_post_id(cls, post_app_id):
        if isinstance(post_app_id, str) and re.findall(r"\d+_\d+", post_app_id):
            post_id = post_app_id.split("_")[1]
            return post_id
        else:
            raise TypeError("'post_app_id' is invalid")

    def get_comments(self, next_cursor=None):
        """Get list comment from Facebook post via GraphQL"""
        var_request = cmt_const.FB_GRAPHQL_VAR
        var_request['feedbackID'] = self.post_id
        var_request['before'] = next_cursor
        multipart_data = MultipartEncoder(
            fields={
                'variables': json.dumps(var_request),
                'doc_id': cmt_const.FB_GRAPHQL_DOC_ID
            }
        )
        cmt_const.FB_GRAPHQL_HEADER['content-type'] = multipart_data.content_type
        with Controller.from_port(fb_const.TOR_SERVER, fb_const.TOR_CONTROL_PORT) as controller:
            controller.authenticate(fb_const.TOR_PASSWORD)
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, fb_const.TOR_SERVER, fb_const.TOR_DEFAULT_PORT)
            socket.socket = socks.socksocket
            controller.signal(Signal.NEWNYM)
            response_obj = requests.post(
                url=cmt_const.FB_GRAPHQL_URL,
                data=multipart_data,
                headers=cmt_const.FB_GRAPHQL_HEADER
            )
        try:
            comment_obj = response_obj.json()['data']['feedback']['display_comments']
        except Exception:
            if "errors" in response_obj.json():
                time.sleep(3)
                self.counter += 1
                if self.counter < 2:
                    self.get_comments(next_cursor)
                else:
                    raise ErrorRequestFormat(str(response_obj.json()))
        else:
            self.transform_list_comments(comment_obj)
        return self.list_comment, self.cursor

    def transform_list_comments(self, comment_obj, parent_id=None):
        """Transform list comment for FB GraphQL"""
        list_cmt = comment_obj['edges'] if isinstance(comment_obj, dict) and len(comment_obj['edges']) > 0 else []
        for cmt in list_cmt:
            if parent_id:
                cmt['node']['parent_id'] = parent_id
            cmt_obj, list_reply = self.transform_comment(cmt['node'])
            self.list_comment.append(cmt_obj)
            if list_reply:
                self.transform_list_comments(list_reply, parent_id=cmt_obj['comment']['_id'])

        if not parent_id:
            paging = comment_obj.get('page_info')
            if paging and paging.get('has_previous_page'):
                self.cursor['has_next_page'] = True
                self.cursor['next_cursor'] = paging.get('start_cursor')

    def transform_comment(self, cmt):
        """Transform comment for FB GraphQL"""
        parsed_cmt = {'comment': {}}
        parsed_cmt['comment']['_id'] = cmt.get('legacy_token')
        parsed_cmt['comment']['fbid'] = cmt.get('legacy_fbid')
        parsed_cmt['comment']['post_id'] = self.post_id
        parsed_cmt['comment']['created_time'] = str(datetime.fromtimestamp(cmt.get('created_time', 0)))
        parsed_cmt['comment']['taken_at_timestamp'] = cmt.get('created_time', 0)
        parsed_cmt['comment']['message'] = cmt['body'].get("text") if cmt.get('body') else ""
        parsed_cmt['comment']['num_reaction'] = cmt['feedback']['reactors'].get("count") \
            if cmt.get('feedback') else 0
        # Get sticker if have
        if cmt.get('attachments'):
            parsed_cmt['comment']['sticker'] = cmt['attachments'][0]['sticker']['sticker_image'].get("uri") \
                if cmt['attachments'][0]['sticker'].get('sticker_image') \
                else ""
        # Get 'parent id' if have
        if cmt.get('parent_id'):
            parsed_cmt['comment']['parent_comment_id'] = cmt.get('parent_id')

        # Get "commenter" info
        if cmt.get('author'):
            user_type = cmt['author'].get('__typename', "user").lower()
            parsed_cmt[user_type] = {}
            if user_type == 'user':
                parsed_cmt[user_type]["_id"] = int(cmt['author']['id'])
            else:
                parsed_cmt[user_type]["app_id"] = int(cmt['author']['id'])
            parsed_cmt['comment']['user_id'] = int(cmt['author']['id'])
            parsed_cmt[user_type]["full_name"] = cmt['author'].get('name')
            parsed_cmt[user_type]["avatar"] = cmt['author']['profile_picture_depth_0'].get('uri')
            page_url = cmt['author']['url'] if cmt['author'].get('url') else cmt['author']['id']
            username = re.findall(r"https://www.facebook.com/(\S+)", page_url)
            parsed_cmt[user_type]['username'] = username[0] if username and \
                                                               ('-' not in username or 'people' not in username) \
                else str(cmt['author']['id'])
        list_reply = cmt['feedback'].get('display_comments', [])
        return parsed_cmt, list_reply
