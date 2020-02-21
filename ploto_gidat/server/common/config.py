import yaml
from loguru import logger


class Config(object):
    def __init__(self, config_path: str):
        with open(config_path) as config_file:
            config_dict = yaml.safe_load(config_file)
            server_config = config_dict['server']
            self.SERVER_CONFIG = config_dict

            if 'debug' in server_config:
                debug_config = server_config['debug']
                if 'flask_debug' in debug_config:
                    flask_debug = debug_config['flask_debug']
                    if flask_debug is True:
                        self.DEBUG = True
                    elif flask_debug is not True:
                        self.DEBUG = False

    @classmethod
    def load_config(cls, config_file_path: str):
        logger.info(f"config file path: {config_file_path}")

        config_object = Config(config_file_path)

        return config_object
