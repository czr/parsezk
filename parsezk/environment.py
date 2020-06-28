class Config(object):
    """Key/value store for configuration data"""

    config = {}

    def get(key):
        return Config.config[key]

    def set(key, value):
        Config.config[key] = value
