class ParserException(Exception):
    message = "Failed to parse XML!"
    type = "parser_error"

    def __init__(self, reason: str):
        self.reason = reason


class SchemaException(Exception):
    message = "Failed to validate XML against schema!"
    type = "schema_error"

    def __init__(self, reason: str):
        self.reason = reason


class VerifyException(Exception):
    message = "Failed to verify XML!"
    type = "verify_error"

    def __init__(self, reason: str):
        self.reason = reason
