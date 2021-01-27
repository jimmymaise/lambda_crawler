import re
import requests
import dateparser
import functions.social_networks.facebook.post_comment.constants.comment as cmt_const
from core.utils.exceptions import ErrorRequestFormat


class GraphApiHandler:
    """Class for comment collection via FB Graph API - Only for Facebook Page"""
    def __init__(self, post_app_id: str, token: str):
        self.post_app_id = post_app_id
        self.token = token
        self.list_cmt = []
        self.cursor = {'has_next_page': False, 'next_cursor': None}

    def get_comments(self, next_cursor=None):
        """Get list comment of post from FB Graph API - Only for FB Page"""
        self._check_requirements()
        url = cmt_const.FB_GRAPH_API_URL % (self.post_app_id,
                                            ','.join(cmt_const.FB_GRAPH_API_VAR),
                                            self.token)
        if next_cursor:
            url = url + next_cursor
        self._get_list_cmt_from_graph_api(url)
        return self.list_cmt, self.cursor

    def _check_requirements(self):
        """Check type of requirements: 'post_app_id' and 'token'"""
        if isinstance(self.post_app_id, str):
            if not re.findall(r"\d+_\d+", self.post_app_id):
                raise TypeError("'post_app_id' is invalid")
        else:
            raise TypeError("'post_app_id' is invalid")
        if not isinstance(self.token, str):
            raise TypeError("'token' is invalid")

    def _get_list_cmt_from_graph_api(self, url):
        """Get list comment of post via FB Graph API - Only for Facebook Page"""
        response_obj = requests.get(url)
        response_data = response_obj.json()

        # If have data
        if response_data.get('data'):
            self.list_cmt += self._transform_list_comment(response_data['data'])
            # If have more comment
            if response_data.get('paging') and response_data['paging'].get('next'):
                self.cursor['has_next_page'] = True
                self.cursor['next_cursor'] = response_data['paging']['cursors']['after']
        # If have errors
        if response_data.get('error'):
            print(response_data.get('error'))
            error_message = response_data['error']['message']
            raise ErrorRequestFormat(error_message)

    def _transform_list_comment(self, list_cmt):
        """Transform list comments from FB Graph API - Only for FB page"""
        list_transformed_cmt = list()
        for cmt in list_cmt:
            transformed_cmt = self._transform_comment(cmt)
            list_transformed_cmt.append(transformed_cmt)
        return list_transformed_cmt

    @classmethod
    def _transform_comment(cls, cmt):
        """Transform comment from FB Graph API - Only for FB page"""
        parsed_cmt = {'comment': {}}

        # --- Parse comment ID ---
        parsed_cmt['comment']['_id'] = cmt['id']
        # --- Parse post_id + fbid (+ 'parent ID' if have) ---
        parsed_cmt['comment']['fbid'] = int(cmt['id'].split('_')[-1])
        parsed_cmt['comment']['post_id'] = int(cmt['id'].split('_')[0])
        if cmt.get('parent'):
            parsed_cmt['comment']['parent_comment_id'] = cmt['parent'].get('id')
        # --- Parse content ---
        parsed_cmt['comment']['message'] = cmt.get('message', "")

        # --- Parse created time ---
        parsed_cmt['comment']['created_time'] = cmt.get('created_time')
        parsed_cmt['comment']['taken_at_timestamp'] = int(dateparser.parse(cmt.get('created_time')).timestamp())

        # --- Parse num reaction ---
        parsed_cmt['comment']['num_reaction'] = cmt.get('like_count', 0)

        # Parse sticker (if have)
        if cmt.get('attachment'):
            parsed_cmt['comment']['sticker'] = cmt['attachment'].get('url')\
                                               if cmt['attachment'].get('type') == "sticker" else None

        # --- Parse page info (if have) ---
        if cmt.get('from'):
            parsed_cmt['page'] = {}
            parsed_cmt['page']['app_id'] = int(cmt['from'].get('id', 0))
            parsed_cmt['comment']['user_id'] = int(cmt['from'].get('id'))
            parsed_cmt['page']['full_name'] = cmt['from'].get('name')
            parsed_cmt['page']['username'] = cmt['from'].get('username', parsed_cmt['page']['app_id'])
        return parsed_cmt
