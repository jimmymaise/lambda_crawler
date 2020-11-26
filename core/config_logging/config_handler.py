import copy
import json
import os

from core.constants.core_constant import CoreConst

etl_folder_path = None
etl_config = None


class BaseConfig:

    def __init__(self):
        pass

    @staticmethod
    def is_local():
        return os.getenv('ENV', '').upper() == 'LOCAL'

    @classmethod
    def init_config(cls, etl_path):
        global etl_config
        global etl_folder_path
        etl_folder_path = etl_path
        etl_const_config_path = os.path.join(etl_path, CoreConst.CONFIG_FILE_PATH)
        with open(etl_const_config_path, 'r') as const_config_file:
            const_config_str = const_config_file.read()
            etl_config = json.loads(const_config_str)
        return cls.get_config()

    @staticmethod
    def get_config():
        global etl_config
        if not etl_config:
            raise ValueError('Need to init config')
        return copy.deepcopy(etl_config)

    @staticmethod
    def get_etl_folder_path():
        global etl_folder_path
        if not etl_folder_path:
            raise ValueError('Cannot get etl folder path')
        return etl_folder_path
