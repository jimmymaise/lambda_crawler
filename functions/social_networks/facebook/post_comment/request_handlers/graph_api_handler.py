import re
import requests
import dateparser
import core.constants.base_facebook_constant as fb_const
import functions.social_networks.facebook.post_comment.constants.comment as cmt_const

class GraphHandler:
    "Class for comment collection via FB Graph API - Only for Facebook Page"
    def __init__(self, post_app_id: str, token: str):
        self.post_app_id = post_app_id
        self.token = token
        self.list_cmt = []

    def get_comments(self):
        "Get list comment of post from FB Graph API - Only for FB Page"
        self.__check_requirements()
        url = cmt_const.FB_GRAPH_API_URL % (self.post_app_id,
                                            ','.join(cmt_const.FB_GRAPH_API_VAR),
                                            self.token)
        self.__get_list_cmt_from_graph_api(url)
        return self.list_cmt

    def __check_requirements(self):
        "Check type of requirements: 'post_app_id' and 'token'"
        if isinstance(self.post_app_id, str) and isinstance(self.token, str):
            if not re.findall(r"\d+\_\d+", self.post_app_id):
                raise TypeError("'post_app_id' is invalid")
        else:
            raise TypeError("'post_app_id' / 'token' is invalid")

    def __get_list_cmt_from_graph_api(self, url):
        'Get list comment of post via FB Graph API - Only for Facebook Page'
        response_obj = requests.get(url)
        response_data = response_obj.json()

        # If have data
        if response_data.get('data'):
            self.list_cmt += self.__transform_list_comment(response_data['data'])
            # If have more comment
            if response_data.get('paging') and response_data['paging'].get('next'):
                self.__get_list_cmt(response_data['paging']['next'])

        # If have errors
        if response_data.get('error')
            error_message = response_data['error']['message']
            raise Exception(error_message)

    def __transform_list_comment(self, list_cmt):
        'Transform list comments from FB Graph API - Only for FB page''
        list_transformed_cmt = []
        for cmt in list_cmt:
            transformed_cmt, reply_cmt = self.__transform_comment(cmt)
            list_transformed_cmt.append(transformed_cmt)
            if reply_cmt:
                transformed_rcmt = self.__transform_list_comment(reply_cmt)
                list_transformed_cmt += transformed_rcmt
        return list_transformed_cmt

    @classmethod
    def __transform_comment(cls, cmt):
        'Transform comment from FB Graph API - Only for FB page'
        parsed_cmt = {}

        # --- Parse comment ID ---
        parsed_cmt['_id'] = cmt['id']

        # --- Parse post_id & fbid ---
        parsed_cmt['fbid'] = int(parsed_cmt['_id'].split('_')[-1])
        parsed_cmt['post_id'] = int(parsed_cmt['_id'].split('_')[0])

        # --- Parse content ---
        parsed_cmt['message'] = cmt.get('message', "")

        # --- Parse created time ---
        parsed_cmt['created_time'] = cmt.get('created_time', 0)
        parsed_cmt['taken_at_timestamp'] = int(dateparser.parse(parsed_cmt['created_time']))

        # --- Parse num reaction ---
        parsed_cmt['num_reaction'] = cmt.get('like_count', 0)

        # --- Parse user info (if have) ---
        if cmt.get('from'):
            parsed_cmt['user_id'] = int(cmt['from'].get('id'))
            parsed_cmt['full_name'] = cmt['from'].get('name')
        else:
            parsed_cmt['user_id'] = 0
            parsed_cmt['full_name'] = ""

        # Parse sticker (if have)
        if cmt.get('attachment'):
            parsed_cmt['sticker'] = cmt['attachment'].get('url')\
                                    if cmt['attachment'].get('type') == "sticker" else None
        # Get reply comment (if have)
        cmt_reply = cmt['comments']['data'] if cmt.get('comments') else None
        
        return parsed_cmt, cmt_reply