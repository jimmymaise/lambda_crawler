import sys
from pathlib import Path

from core.deployment.base_deploy_handler import BaseDeployHandler
from functions.social_networks.instagram.post_comment.config_logging.config_handler import Config

sys.path.append(str(Path(__file__).resolve().parents[4]))
function_path = str(Path(__file__).resolve().parents[1])


class DeployCode:
    def __init__(self):
        self.config = Config.init_config(function_path=function_path)
        self.deploy_handler = BaseDeployHandler()

    def deploy(self):
        self.deploy_handler.deploy_code()

    def main(self):
        self.deploy()


if __name__ == '__main__':
    DeployCode().main()
