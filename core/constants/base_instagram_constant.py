class LambdaResquestConst:
    DATA_FIELDS = 'data_fields'


class IGResponseConst:
    HAS_NEXT_PAGE = 'has_next_page'
    END_CURSOR = 'end_cursor'
    PAGE_INFO = 'page_info'
    NODE = 'node'
    EDGES = 'edges'
    STATUS_CODE = 'status_code'


class LambdaResponseConst:
    STATUS_CODE = 'status_code'
    BODY = 'body'
    CURSOR = 'cursor'
    MESSAGE = 'message'


class IGBaseURLConstant:
    BASE_INSTAGRAM_PAGING_URL = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables='
