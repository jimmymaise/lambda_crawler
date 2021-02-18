from core.constants.core_constant import CoreConst


class NotAFileError(Exception):
    def __init__(self, message=CoreConst.NOT_A_FILE_ERROR_MESSAGE):
        self.message = message

    def __str__(self):
        return self.message


class ErrorRequestFormat(Exception):
    def __init__(self, message='ErrorRequestFormat'):
        self.message = message
        self.collection_service_error_name = 'error_request_format'

    def __str__(self):
        return self.message


class ErrorSocialType(Exception):
    """Class for Error Exception: Social type is invalid"""
    def __init__(self, message='Social type is invalid'):
        self.message = message
        self.collection_service_error_name = 'error_post_details'

    def __str__(self):
        return self.message


class PostNotFoundError(Exception):
    """Class for Error Exception: Post can not access - Has been deleted or private access"""
    def __init__(self, message="Post isn't available right now"):
        self.message = message
        self.collection_service_error_name = 'error_post_details'

    def __str__(self):
        return self.message
