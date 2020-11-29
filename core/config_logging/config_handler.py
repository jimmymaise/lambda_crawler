import copy
import json
import os

from core.constants.core_constant import CoreConst

function_folder_path = None
function_config = None


class BaseConfig:

    def __init__(self):
        pass

    @staticmethod
    def is_local():
        return os.getenv('ENV', '').upper() == 'LOCAL'

    @classmethod
    def init_config(cls, function_path):
        global function_config
        global function_folder_path
        function_folder_path = function_path
        function_const_config_path = os.path.join(function_path, CoreConst.CONFIG_FILE_PATH)
        with open(function_const_config_path, 'r') as const_config_file:
            const_config_str = const_config_file.read()
            function_config = json.loads(const_config_str)
        return cls.get_config()

    @staticmethod
    def get_config():
        global function_config
        if not function_config:
            raise ValueError('Need to init config')
        return copy.deepcopy(function_config)

    @staticmethod
    def get_function_folder_path():
        global function_folder_path
        if not function_folder_path:
            raise ValueError('Cannot get function folder path')
        return function_folder_path
