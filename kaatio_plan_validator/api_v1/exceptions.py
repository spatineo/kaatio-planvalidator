class ParserException(Exception):
    type = "parser_error"


class SchemaException(Exception):
    type = "schema_error"


class VerifyException(Exception):
    type = "verify_error"
