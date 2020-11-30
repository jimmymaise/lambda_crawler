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
        self.paging_handler = CommentPagingHandler()
        self.comment_request_body = IGCommentPaginateRequestSchema().load(self.event)

    def crawl_ig_comments(self):
        request_params = {
            CommentConst.TIMEOUT: self.config['timeout'],
            CommentConst.QUERY_HASH: self.comment_request_body['query_hash'],
            CommentConst.CURSOR: self.comment_request_body.get(CommentConst.CURSOR),
            CommentConst.COOKIES: self.comment_request_body[CommentConst.COOKIES],
            CommentConst.SHORTCODE: self.comment_request_body[CommentConst.SHORTCODE],
            CommentConst.NUM_ITEM: self.comment_request_body[CommentConst.NUM_ITEM],
        }
        url_options = PagingCommentUrlOptionsSchema().load(request_params)
        request_options = PagingCommentRequestOptionsSchema().load(request_params)

        return self.paging_handler.do_paging_request(url_options, request_options)


def lambda_handler(event, context):
    return MainStep(event, context).crawl_ig_comments()


if __name__ == '__main__':
    # Just for testing. Remove it
    event_test = {"data_fields": {"shortcode": 'CEiuPKTF9cA',
                                  "cursor": "QVFEam9QUnIxbjNtREN4TTFkSEJsbXVaR3lodENGX2ozT3dxazVSSHdWMmZ5Q1VJaFRlbW1wTjFlLVlQNzhNS29TbTBjd1c2WkNpM3JHV3laRjBfeUdjbA==",
                                  "num_item": 15,
                                  "query_hash": "bc3296d1ce80a24b1b6e40b1e72903f5"
                                  },
                  "cookies": {"csrftoken": "nWQDjZR15gg18NDkMYo64DOo9TIiE6uq", "ds_user_id": "4026520510",
                              "ig_did": "590E4533-964D-48E4-8EB1-A57F83508AFB", "mid": "XpU29wALAAGyV7cDF8TSJ7z_3R6I",
                              "rur": "FRC", "sessionid": "4026520510%3AQ7ZQdKMJFVdHSi%3A23", "shbid": "14922",
                              "urlgen": "{'115.78.0.111': 7552}:1jiXX6:Fyopguky-ncqo3WyxfM-6S3O8YU"}}

    response = lambda_handler(event=event_test, context=None)
    import json

    print(json.dumps(response))
