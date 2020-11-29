# BASE URLs
class IGBaseURLConstant:
    BASE_INSTAGRAM_PAGING_URL = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables='
    BASE_INSTAGRAM_GET_ONE_ITEM_DETAIL_URL = 'https://www.instagram.com/{item_id}/?__a=1'


# Lambda Request
class LambdaRequestConst:
    DATA_FIELDS = 'data_fields'


# Lambda Response
class LambdaResponseConst:
    STATUS_CODE = 'status_code'
    BODY = 'body'
    CURSOR = 'cursor'
    MESSAGE = 'message'


# IG Request
class IGResponseConst:
    HAS_NEXT_PAGE = 'has_next_page'
    END_CURSOR = 'end_cursor'
    PAGE_INFO = 'page_info'
    NODE = 'node'
    EDGES = 'edges'
    STATUS_CODE = 'status_code'
