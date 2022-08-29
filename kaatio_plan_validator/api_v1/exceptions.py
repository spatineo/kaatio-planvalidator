class ParserException(Exception):
    def __init__(self, message: str, reason: str):
        self.message = message
        self.reason = reason


class SchemaException(Exception):
    def __init__(self, message: str, reason: str):
        self.message = message
        self.reason = reason


class ValidateException(Exception):
    def __init__(self, message: str, reason: str):
        self.message = message
        self.reason = reason
