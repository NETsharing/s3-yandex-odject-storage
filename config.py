import os
import configparser


class Config:
    # _CONFIG_NAME = None
    _CONFIG_NAME = 'config.ini'

    def __init__(self):

        self.options = {
            'logging': {
                'log_path': None,
                'log_level': 'DEBUG',
                'log_format': '%(asctime)s - %(levelname)s - %(message)s'
            },
            'db': {
                'postgres': None
            },
            'general': {
                'chunk_step': None,
                'promts_table': 'promts',
                'promts_files_table':'promt_files'
            }
        }
        self._parseini()

    def _parseini(self):
        if self._CONFIG_NAME is None:
            return

        path = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(path + '/' + self._CONFIG_NAME):
            return

        conf = configparser.RawConfigParser()
        conf.read(path + '/' + self._CONFIG_NAME)

        for key, value in conf.items():
            if key in self.options:
                self.options[key] = dict(value)

    def __getitem__(self, key):
        if key in self.options:
            return self.options[key]
        return {}
