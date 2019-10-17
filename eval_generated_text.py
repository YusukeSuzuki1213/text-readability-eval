import textstat
import configparser


 DEFAULT_CONFIG_FILE = "./config.ini"

class ConfigUtil():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(DEFAULT_CONFIG_FILE)

    def getConfig(self) :
        return self.config


# ARIで評価
textstat.automated_readability_index("")



