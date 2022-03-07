class ConfigException(Exception):
    """Base config exception"""
    def __init__(self, message="Config file has errors"):
        self.message = message
        super().__init__(self.message)


class ConfigFileDoesNotExist(ConfigException):
    """Config file does not exist exception"""
    def __init__(self, message="Config file does not exist"):
        self.message = message
        super().__init__(self.message)


class ConfigMissingFields(ConfigException):
    """Config file doesn't have some fields inside exception"""
    def __init__(self, message="Config file doesn't have some fields inside"):
        self.message = message
        super().__init__(self.message)


class DialogNotFound(Exception):
    """Dialog with the name is not found"""
    def __init__(self, message="Chat with the given name is not found"):
        self.message = message
        super().__init__(self.message)
