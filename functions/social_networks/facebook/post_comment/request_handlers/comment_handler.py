"""
Post handler for crawl user + post info from HTML
"""
import re
from http import HTTPStatus
import requests
import socks
import socket
from stem import Signal
from stem.control import Controller
from core.constants.core_constant import CoreConst
from core.utils.exceptions import PostNotFoundError
import core.constants.base_facebook_constant as fb_constant
from core.handlers.crawl_account_handler import CrawlAccountHandler
import functions.social_networks.facebook.post_comment.constants.comment as cmt_const_module
from functions.social_networks.facebook.post_comment.request_handlers.graph_api_handler import GraphHandler
from functions.social_networks.facebook.post_comment.request_handlers.graphql_api_handler import GraphQLHandler



class CommentHandler:
    "Class for post collection with HTTP request"
    def __init__(self, post_app_id: str, account_info: dict, social_type='facebook'):
        self.post_app_id = post_app_id
        self.account_info = account_info
        self.social_type = social_type
        self.list_comment = []

    def get_list_comment(self):
        "Get list post's comment from FB Graph API / FB GraphQL API"
        response_fields = fb_constant.LambdaResponseConst
        token_str = self.account_info.get('info')
        list_comment = GraphHandler(self.post_app_id, token_str).get_comments()\
                       if self.social_type == 'facebook_page'
                       else GraphQLHandler(self.post_app_id).get_comment()
        result = {
            response_fields.POST_FIELD: {
                response_fields.CMT_FIELD: list_comment
            }
        }
        return result
