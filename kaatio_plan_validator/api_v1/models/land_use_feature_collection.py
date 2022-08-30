from __future__ import annotations

import warnings
from typing import Any

import lxml.etree as ET
import xmlschema
from pydantic import validator

from .. import constants, exceptions
from . import common

warnings.simplefilter(action="ignore", category=xmlschema.XMLSchemaImportWarning)


class LandUseFeatureCollection(common.XmlModel):
    """Represents model definition for LandUseFeatureCollection class."""

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def parse_xml(cls, source: Any, **kwargs):
        """Create instance from source XML."""

        try:
            return cls(
                xml=ET.parse(source),
                **kwargs,
            )
        except ET.ParseError as exc:
            raise exceptions.ParserException(
                reason=str(exc),
            )

    @validator("xml")
    def xml_must_be_xsd_valid(cls, xml: ET._ElementTree, values: dict[str, Any]):
        """XML document must validate against XSD."""

        try:
            skip: dict = values.get("skip")
            if not skip.get("no_xsd_validation"):
                xsd = xmlschema.XMLSchema(
                    constants.SCHEMA_FILES,
                    allow="sandbox",
                    base_url=str(constants.SCHEMA_DIR),
                    defuse="always",
                )

                xsd.validate(xml)
            return xml
        except xmlschema.XMLSchemaException as err:
            raise exceptions.SchemaException(
                reason=str(err),
            )

    def find_feature_members_by_tag(self, tag: str) -> list[ET._Element]:
        return [
            fm
            for fms in list(self.xml.getroot())
            for fm in list(fms)
            if isinstance(fm, ET._Element) and fm.xpath(constants.XPATH_LOCAL_NAME) == tag
        ]

    def to_string(self) -> str:
        return ET.tostring(self.xml, encoding="unicode", pretty_print=True)
