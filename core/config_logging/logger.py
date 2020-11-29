import logging
import os
import pathlib
import sys

from core.constants.core_constant import CoreConst

global_logger_name = CoreConst.TOP_LEVEL_SCOPE
is_set_console_for_top_level_scope = False
sensitive_info = set()


class Logger:
    is_running_lambda_logging = bool(os.getenv('CORE_LAMBDA_FRAMEWORK'))

    def __init__(self):
        self.app_logger = logging

    @staticmethod
    def _add_custom_log_level(logger, name, level_code):
        logging.addLevelName(level_code, name.upper())
        setattr(logger, name.lower(), lambda message, *args: getattr(logger, '_log')(level_code, message, args))

    @classmethod
    def _add_multiple_log_level(cls, logger, custom_log_dict_list):
        for custom_log_dict in custom_log_dict_list:
            cls._add_custom_log_level(logger=logger, name=custom_log_dict['name'],
                                      level_code=custom_log_dict['code'])

    def _hook_handle_uncaught_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        self.app_logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    @staticmethod
    def _setup_logger_console(logger, is_use_color_log=True):

        # Just need to display in console when running task file directly
        # define a Handler which writes INFO messages or higher to the sys.stderr

        console = logging.StreamHandler(sys.stdout)

        console.setLevel(logging.INFO)
        logger.addHandler(console)

    def init_deployment_logger(self, logger_name, log_file_path):
        return self.init_logger(logger_name, log_file_path)

    @staticmethod
    def add_log_file_handler(logger, log_file_path, mode, level, log_format):
        log_handler = logging.FileHandler(
            filename=log_file_path, mode=mode)
        log_handler.setLevel(level)
        log_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(log_handler)

    def init_logger(self, logger_name, log_file_path=None, remove_old_log=False):
        log_level = logging.INFO
        log_format = CoreConst.LOG_FORMAT
        logger = logging.getLogger(logger_name)
        if log_file_path:
            os.makedirs(pathlib.Path(log_file_path).resolve().parents[0], exist_ok=True)
            normal_log_file_path = '{}.log'.format(log_file_path)
            error_log_file_path = '{}_error.log'.format(log_file_path)
            mode = 'w' if remove_old_log else 'a'

            logging.basicConfig(format=log_format,
                                filename=normal_log_file_path,
                                level=log_level, datefmt='%Y-%m-%d %H:%M:%S')

            self.add_log_file_handler(logger=logger, level=logging.ERROR, log_file_path=error_log_file_path,
                                      mode=mode, log_format=log_format)

        else:
            logging.basicConfig(format=log_format,
                                level=log_level, datefmt='%Y-%m-%d %H:%M:%S')
        if self.is_running_lambda_logging:
            logger.setLevel(logging.INFO)
        else:
            self._setup_logger_console(logger)

        logger.info('*********************INIT LOGGING***********************')
        self.app_logger = logger

        sys.excepthook = self._hook_handle_uncaught_exception
        global global_logger_name
        global_logger_name = logger_name
        return logger

    @classmethod
    def get_logger(cls):
        global global_logger_name
        global is_set_console_for_top_level_scope
        logger = logging.getLogger(global_logger_name or '')
        if not is_set_console_for_top_level_scope and global_logger_name == CoreConst.TOP_LEVEL_SCOPE:
            is_set_console_for_top_level_scope = True
            logger.setLevel(logging.INFO)
            if not cls.is_running_lambda_logging:
                cls._setup_logger_console(logger)
        return logger
