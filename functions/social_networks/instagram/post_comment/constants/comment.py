from core.constants.base_instagram_constant import IGBaseURLConstant


class CommentConst:
    COMMENT_URL_NO_CURSOR = IGBaseURLConstant.BASE_INSTAGRAM_PAGING_URL + '{{"shortcode": "{shortcode}", "first": {num_item}}}'
    COMMENT_URL_WITH_CURSOR = IGBaseURLConstant.BASE_INSTAGRAM_PAGING_URL + '{{"shortcode": "{shortcode}", "first": {num_item},' \
                                                                            '"after":"{cursor}"}}'
    COMMENT_DATA_RESPONSE_KEY_PATH = ['data', 'shortcode_media', 'edge_media_to_parent_comment']
    CONST_CONFIG_FILE_PATH = 'config/config.json'
    COMMENT_RESOURCE_TYPE = 'COMMENT'
    MAX_NUM_ITEM = 'max_num_comments'
    NUM_ITEM = 'num_item'
    TIMEOUT = 'timeout'
    QUERY_HASH = 'query_hash'
    CURSOR = 'cursor'
    COOKIES = 'cookies'
    SHORTCODE = 'shortcode'
