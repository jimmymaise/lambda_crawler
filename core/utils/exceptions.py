from core.constants.core_constant import CoreConst


class NotAFileError(Exception):
    def __init__(self, message=CoreConst.NOT_A_FILE_ERROR_MESSAGE):
        self.message = message

    def __str__(self):
        return self.message
