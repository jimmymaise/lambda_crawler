"""
Constants for get comment info from post
"""

FB_GRAPHQL_URL = "https://www.facebook.com/api/graphql/"
FB_GRAPHQL_VAR = {
    "after":None,
    "before":None,
    "feedbackID":None,
    "feedLocation": "PERMALINK",
    "feedbackSource":50,
    "first":None,
    "focusCommentID":None,
    "includeNestedComments":True,
    "isComet":False,
    "last":50,
    "scale":1.5,
    "topLevelViewOption":None,
    "useDefaultActor":True,
    "viewOption":"RANKED_UNFILTERED",
    "UFI2CommentsProvider_commentsKey":"CometSinglePostRoute",
    "UFI2CommentsProviderPaginationQuery": None
}
FB_GRAPHQL_DOC_ID = "4629548627085906"
FB_GRAPHQL_HEADER = {
    'content-type': multipart_data.content_type,
    "user-agent": "insomnia/2020.5.2"  
}

FB_GRAPH_API_URL = 'https://graph.facebook.com/v9.0/%s/comments?limit=1000&filter=stream&fields=%s&access_token=&s'
FB_GRAPH_API_VAR = [
    "id",
    "message",
    "from{id, name}",
    "comments{id,message,from{id, name},is_hidden,created_time,like_count,attachments{type,url}}",
    "created_time",
    "is_hidden",
    "like_count",
    "attachments{type,url}"
]
