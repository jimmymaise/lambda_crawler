class CoreConst:
    LOG_FORMAT = '%(asctime)s - %(name)s: [%(levelname)s]: %(message)s'
    BASE_INSTAGRAM_PAGING_URL = 'https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables='
    COMMENT_URL_NO_CURSOR = BASE_INSTAGRAM_PAGING_URL + '{{"shortcode": "{shortcode}", "first": {num_item}}}'
    COMMENT_URL_WITH_CURSOR = BASE_INSTAGRAM_PAGING_URL + '{{"shortcode": "{shortcode}", "first": {num_item},' \
                                                          '"after":"{cursor}"}}'
    CONFIG_FILE_PATH = 'config_logging/config.json'
    COMMENT_RESOURCE_TYPE = 'COMMENT'
    POST_RESOURCE_TYPE = 'POST'

    BASE_INSTAGRAM_GET_ONE_ITEM_DETAIL_URL = 'https://www.instagram.com/{item_id}/?__a=1'

    SLACK_NOTIFICATION_HOOK_URL = "https://hooks.slack.com/services/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"
