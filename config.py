import configparser
import os

configParser = configparser.RawConfigParser()
configFilePath = "config.ini"
configParser.read(configFilePath)


def cfg(section, key, casting=str):
    var_env = str(section+"_"+key).upper()
    # Give the environment variable a shot before using the config file
    if var_env in os.environ:
        return os.environ[var_env]
    return casting(configParser.get(section, key))
