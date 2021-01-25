import json
import re
import time
import dateparser
import requests
import socks
import socket
from stem import Signal
from stem.control import Controller
import core.constants.base_facebook_constant as fb_const
import functions.social_networks.facebook.post_comment.constants.comment as cmt_const

class GraphQLHandler:
    "Class for comment collection via FB GraphQL API"
    def __init__(self, post_app_id: str):
        self.post_id = post_app_id.split("_")[1]
        self.list_comment = []

    def get_comments(self, next_cursor=None):
        "Get list comment from Facebook post via GraphQL"
        var_request = cmt_const.FB_GRAPHQL_VAR
        var_request['feedbackID'] = self.post_id
        var_request['before'] = next_cursor
        multipart_data = MultipartEncoder(
            fields={
                'variables': json.dumps(var_request),
                'doc_id': cmt_const.FB_GRAPHQL_DOC_ID
            }
        )
        with Controller.from_port(fb_const.TOR_SERVER, fb_const.TOR_CONTROL_PORT) as controller:
            controller.authenticate(fb_const.TOR_PASSWORD)
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, fb_const.TOR_SERVER, fb_const.TOR_DEFAULT_PORT)
            socket.socket = socks.socksocket
            controller.signal(Signal.NEWNYM)
            response_obj = requests.post(url=CMT_URL, data=multipart_data,
                                         headers=cmt_const.FB_GRAPHQL_HEADER
                                        )
        try:
            comment_obj = response_obj.json()['data']['feedback']['display_comments']
        except Exception:
            if "errors" in response_obj.json():
                time.sleep(3)
                self.get_list_cmt(next_cursor)
        else:
            self.transform_list_comments(comment_obj)
        return self.list_comment

    def transform_list_comments(self, comment_obj):
        "Transform list comment for FB GraphQL"
        if type(comment_obj) != dict:
            print(comment_obj)
        cmts = comment_obj['edges'] if comment_obj and len(comment_obj['edges']) > 0 else []
        for cmt in cmts:
            cmt_obj = self.transform_comment(cmt['node'])
            if cmt_obj:
                self.list_comment.append(cmt_obj)

        paging = comment_obj.get('page_info')
        if paging and paging.get('start_cursor'):
            time.sleep(3)
            self.get_list_cmt(next_cursor=paging.get('start_cursor'))

    @classmethod
    def transform_comment(cls, cmt):
        "Transform comment for FB GraphQL"
        created_date = cmt.get('created_time', 0)
        comment_details = {
            "_id": cmt.get('legacy_token'),
            "fbid": cmt.get('legacy_fbid', -1),
            "created_time": str(datetime.fromtimestamp(created_date)),
            "taken_at_timestamp": created_date,
            "message": cmt['body'].get("text") if cmt.get('body') else "",
        }
        # Get user info 
        if cmt.get('author'):
            comment_details['user_id'] = int(cmt['author']['id'])
            comment_details['full_name'] = cmt['author'].get('name')
            page_url = cmt['author'].get('url', str(cmt['author']['id']))
            username = re.findall(r"https://www.facebook.com\/(\S+)", page_url)
            comment_details['username'] = username[0] if username else str(cmt['author']['id'])
            
            
        # Get sticker if have
        attach_obj = cmt.get('attachments')
        if attach_obj:
            comment_details['sticker'] = attach_obj[0]['sticker']['sticker_image'].get("uri")\
                                        if attach_obj and attach_obj[0]['sticker'].get('sticker_image')\
                                        else ""

        comment_details['num_reaction'] = cmt['feedback']['reactors'].get("count")\
                                          if cmt.get('feedback') else 0
        comment_details['post_id'] = self.post_id

        return comment_details

