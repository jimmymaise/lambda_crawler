class CoreConst:
    TOP_LEVEL_SCOPE = '__main__'
    LOG_FORMAT = '%(asctime)s - %(name)s: [%(levelname)s]: %(message)s'
    CONFIG_FILE_PATH = 'config_logging/config.json'
    FUNC_ID = 'func_id'
    RELATIVE_FUNC = 'relative_func'
    RELATIVE_FUNCTION_PATH_VAR = 'relative_function_path'
    RELATIVE_AWS_TEMPLATE_PATH = '/functions/serverless_templates/aws_serverless_template.yml'

    WRITE_MODE = 'w'

    SERVERLESS_DEFAULT_FILE_NAME = 'serverless.yml'
    REQUIREMENT_DEFAULT_FILE_NAME = 'requirements.txt'

    COMMENT_RESOURCE_TYPE = 'COMMENT'
    POST_RESOURCE_TYPE = 'POST'

    # Third party Notifications
    SLACK_NOTIFICATION_HOOK_URL = "https://hooks.slack.com/services/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"

    # Exception
    NOT_A_FILE_ERROR_MESSAGE = 'NotAFile'

    # Account Manager API
    AM_API = "http://34.219.102.184:9099"
    DEFAULT_PAYLOAD = {
        "api_type": "UPDATE_STATUS",
        "api_body": {
            "social_network": "FACEBOOK",
            "account_ID": "",
            "data": {
                "status_code": 200,
                "message": "Done"
            }
        }
    }