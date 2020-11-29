from core.constants.base_instagram_constant import IGBaseURLConstant


class CommentConst:
    CONST_CONFIG_FILE_PATH = 'config/config.json'

    # URLs
    COMMENT_URL_NO_CURSOR = IGBaseURLConstant.BASE_INSTAGRAM_PAGING_URL + '{{"shortcode": "{shortcode}", "first": {num_item}}}'
    COMMENT_URL_WITH_CURSOR = IGBaseURLConstant.BASE_INSTAGRAM_PAGING_URL + '{{"shortcode": "{shortcode}", "first": {num_item},' \
                                                                            '"after":"{cursor}"}}'
    COMMENT_DATA_RESPONSE_KEY_PATH = ['data', 'shortcode_media', 'edge_media_to_parent_comment']
    COMMENT_RESOURCE_TYPE = 'COMMENT'

    NUM_ITEM = 'num_item'
    TIMEOUT = 'timeout'
    QUERY_HASH = 'query_hash'
    CURSOR = 'cursor'
    COOKIES = 'cookies'
    SHORTCODE = 'shortcode'
