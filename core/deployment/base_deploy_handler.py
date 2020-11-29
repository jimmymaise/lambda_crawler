import os
import subprocess
from pathlib import Path

from jinja2 import Template

from core.config_logging.config_handler import BaseConfig
from core.config_logging.logger import Logger
from core.constants.core_constant import CoreConst
from core.file.file_handler import FileHandler

function_folder_path = None
function_config = ""


class BaseDeployHandler:

    def __init__(self):
        self.logger = Logger.get_logger()
        self.config_data = BaseConfig.get_config()
        self.function_local_folder_path = BaseConfig.get_function_folder_path()
        self.root_path = str(Path(__file__).resolve().parents[2])
        self.relative_elt_path = str(Path(self.function_local_folder_path).relative_to(Path(self.root_path)))
        self.config_data[CoreConst.FUNC_ID] = self.func_id = os.path.basename(self.function_local_folder_path)
        self.config_data[CoreConst.RELATIVE_FUNCTION_PATH_VAR] = self.relative_elt_path
        self.serverless_template_path = CoreConst.RELATIVE_AWS_TEMPLATE_PATH

    def make_yaml_file_from_template(self):
        with open(f'{self.root_path}/{self.serverless_template_path}') as file_content:
            template = Template(file_content.read())
        output = template.render(**self.config_data)
        # to save the results
        output_file_path = f"{self.root_path}/{CoreConst.SERVERLESS_DEFAULT_FILE_NAME}"
        with open(output_file_path, CoreConst.WRITE_MODE) as yaml_deploy_file:
            yaml_deploy_file.write(output)
        return output_file_path

    def copy_requirements_file(self):
        current_file = f'{self.function_local_folder_path}/{CoreConst.REQUIREMENT_DEFAULT_FILE_NAME}'
        dest_file = f'{self.root_path}/{self.config_data[CoreConst.FUNC_ID]}_{CoreConst.REQUIREMENT_DEFAULT_FILE_NAME}'

        FileHandler.copy_file(current_file, dest_file)

    def deploy_code(self):
        # Build template
        self.make_yaml_file_from_template()
        # Copy requirement file
        self.copy_requirements_file()
        # Deploy to s3
        subprocess.run(
            ["serverless", "deploy"], cwd=self.root_path)
