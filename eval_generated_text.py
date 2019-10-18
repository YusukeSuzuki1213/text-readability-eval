import textstat
import configparser
from threading import Lock

CONFIG_FILE = "./config.ini"


class ConfigUtil:
    
    _instance = None
    _lock = Lock() 

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via Constructor')

    @classmethod
    def __internal_new__(cls):
        return super().__new__(cls)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls.__internal_new__()
                    cls._instance.config = configparser.ConfigParser()
                    cls._instance.config.read(CONFIG_FILE)
        return cls._instance


# # ARIで評価
# textstat.automated_readability_index("")
# configUtil = ConfigUtil()
# pconfig = configUtil.getConfig()


if __name__ == '__main__':
    config = ConfigUtil.get_instance().config
    
    print(config.get('Paths','CsvPath'))


