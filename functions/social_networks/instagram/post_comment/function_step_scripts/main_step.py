try:
    import unzip_requirements
except ImportError:
    pass
from pathlib import Path

from functions.social_networks.instagram.post_comment.config_logging.config_handler import Config
from functions.social_networks.instagram.post_comment.constants.comment import CommentConst
from functions.social_networks.instagram.post_comment.request_handlers.comment_paging_handler import \
    CommentPagingHandler
from functions.social_networks.instagram.post_comment.schemas.comment_paging_schema import \
    IGCommentPaginateRequestSchema, PagingCommentUrlOptionsSchema, PagingCommentRequestOptionsSchema

function_path = str(Path(__file__).resolve().parents[1])


class MainStep:
    def __init__(self, event, context):
        self.event = event
        self.context = context
        self.config = Config.init_config(function_path=function_path)
        self.request_body = IGCommentPaginateRequestSchema().load(self.event)

    def crawl_ig_comments(self):
        request_params = {
            CommentConst.TIMEOUT: self.config[CommentConst.TIMEOUT],
            CommentConst.CURSOR: self.request_body.get(CommentConst.CURSOR),
            CommentConst.SHORTCODE: self.request_body[CommentConst.SHORTCODE],
            CommentConst.NUM_ITEM: self.request_body[CommentConst.NUM_ITEM],
            CommentConst.QUERY_HASH: self.request_body[CommentConst.ACCOUNT][CommentConst.QUERY_HASH],
            CommentConst.ACCOUNT_ID: self.request_body[CommentConst.ACCOUNT][CommentConst.ACCOUNT_ID],
            CommentConst.COOKIES: self.request_body[CommentConst.ACCOUNT][CommentConst.COOKIE_FIELD],
        }
        url_options = PagingCommentUrlOptionsSchema().load(request_params)
        request_options = PagingCommentRequestOptionsSchema().load(request_params)
        return CommentPagingHandler(url_options, request_options).do_paging_request()


def lambda_handler(event, context):
    try:
        return MainStep(event, context).crawl_ig_comments()
    except Exception as e:
        fail_param = {
            "isError": True,
            "details": e
        }
        raise RuntimeError(fail_param)


if __name__ == '__main__':
    # Just for testing. Remove it
    event_test = {
        "shortcode": "CKkpGpql4bk",
        "num_item": 50,
        "social_type": "instagram",
        "account_info": {
            "account_id": "accountID_001",
            "query_hash": "bc3296d1ce80a24b1b6e40b1e72903f5",
            "info": {
                "csrftoken": "yvkUNvit4ykNTUqjtDNuYTHVsODBy8pT",
                "datr": "3Wo_Xw2nKCBXzdsCXJspwrnz",
                "ds_user_id": "4026520510",
                "ig_cb": "1",
                "ig_did": "7ECD68B5-8FD8-48D3-AAEA-E2A73A30E568",
                "mid": "XEiL-gALAAH50f_Tc7Kyv0tMXM5C",
                "rur": "FRC",
                "sessionid": "4026520510%3AvrZU5wdcPUkHOZ%3A17",
                "shbid": "14922",
                "shbts": "1610507777.3079073"
            }
        },
        "cursor": None
    }

    response = lambda_handler(event=event_test, context=None)
    import json

    print(json.dumps(response))
