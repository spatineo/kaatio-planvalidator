class ParserException(Exception):
    type = "parser_error"


class SchemaException(Exception):
    type = "schema_error"
