import lxml.etree as ET
import xmlschema

from . import constants, exceptions


def xml_is_xsd_valid(xml: ET._ElementTree) -> bool:
    """Validates given xml against schema."""

    xsd = xmlschema.XMLSchema(
        constants.SCHEMA_FILES,
        allow="sandbox",
        base_url=str(constants.SCHEMA_DIR),
        defuse="always",
    )
    try:
        xsd.validate(xml)
        return True
    except xmlschema.XMLSchemaException as err:
        raise exceptions.ValidatorException(str(err))
