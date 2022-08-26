from __future__ import annotations

from typing import Any

import lxml.etree as ET
import pygml
import xmlschema
from pydantic import BaseModel, validator
from pydantic.utils import GetterDict
from shapely.geometry import shape
from shapely.ops import BaseGeometry

from . import constants, exceptions


class LandUseFeatureCollection(BaseModel):
    """Represents model definition for LandUseFeatureCollection class."""

    skip_xml_must_validate_against_xsd: bool = False
    xml: ET._ElementTree

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
        except ET.ParseError as err:
            raise exceptions.ParserException(str(err))

    @validator("xml")
    def xml_must_validate_against_xsd(cls, xml: ET._Element, values: dict[str, Any]):
        """XML document must validate against XSD."""

        try:
            if not values.get("skip_xml_must_validate_against_xsd"):
                xsd = xmlschema.XMLSchema(
                    constants.SCHEMA_FILES,
                    allow="sandbox",
                    base_url=str(constants.SCHEMA_DIR),
                    defuse="always",
                )

                xsd.validate(xml)
            return xml
        except xmlschema.XMLSchemaException as err:
            raise exceptions.ValidatorException(str(err))

    @validator("xml")
    def xml_has_feature_members(cls, xml: ET._ElementTree):
        """XML document must have feature members."""
        try:
            assert list(xml.getroot())
            return xml
        except AssertionError as err:
            raise exceptions.ValidatorException(str(err))

    def get_feature_members_by_tag(self, tag: str) -> list[ET._Element]:
        """Returns list of feature members."""
        return [
            fm
            for fms in list(self.xml.getroot())
            for fm in list(fms)
            if isinstance(fm, ET._Element) and fm.xpath(constants.XPATH_LOCAL_NAME) == tag
        ]

    @property
    def participation_and_evaluation_plans(self):
        return self.get_feature_members_by_tag("ParticipationAndEvaluationPlan")

    @property
    def plan_objects(self):
        return self.get_feature_members_by_tag("PlanObject")

    @property
    def plan_orders(self):
        return self.get_feature_members_by_tag("PlanOrder")

    @property
    def planners(self):
        return self.get_feature_members_by_tag("Planner")

    @property
    def spatial_plans(self):
        return self.get_feature_members_by_tag("SpatialPlan")


class BaseGetterDict(GetterDict):
    """Represents XPath data binding base class."""

    _obj: ET._Element

    def xpath(self, xpath: str, default: Any) -> Any:
        try:
            return self._obj.xpath(xpath, namespaces=constants.NAMESPACES)[0]
        except IndexError:  # pragma: no cover
            return default


class ParticipationAndEvaluationPlanGetter(BaseGetterDict):
    """Represents dictionary-like interface to execute data binding with ParticipationAndEvaluationPlan class."""

    def get(self, key: str, default: Any) -> Any:

        if key == "gml_id":
            return self.xpath(constants.XPATH_GML_ID, default)
        if key == "producer_specific_identifier":
            return self.xpath(constants.XPATH_PRODUCER_SPECIFIC_IDENTIFIER, default)
        if key == "xml":
            return self._obj
        return default  # pragma: no cover


class ParticipationAndEvaluationPlan(BaseModel):
    """Represents model definition for ParticipationAndEvaluationPlan class."""

    gml_id: str
    producer_specific_identifier: str
    xml: ET._Element

    class Config:
        arbitrary_types_allowed = True
        getter_dict = ParticipationAndEvaluationPlanGetter
        orm_mode = True


class PlanObjectGetter(BaseGetterDict):
    """Represents dictionary-like interface to execute data binding with PlanObject class."""

    def get(self, key: str, default: Any) -> Any:

        if key == "geometry":
            geometry = list(self.xpath(constants.XPATH_GEOMETRY, default))[0]
            return shape(pygml.parse(geometry))
        if key == "gml_id":
            return self.xpath(constants.XPATH_GML_ID, default)
        if key == "producer_specific_identifier":
            return self.xpath(constants.XPATH_PRODUCER_SPECIFIC_IDENTIFIER, default)
        if key == "spatial_plan":
            return self.xpath(constants.XPATH_SPATIAL_PLAN, default)
        if key == "xml":
            return self._obj
        return default  # pragma: no cover


class PlanObject(BaseModel):
    """Represents model definition for PlanObject class."""

    geometry: BaseGeometry
    gml_id: str
    producer_specific_identifier: str
    spatial_plan: str
    xml: ET._Element

    class Config:
        arbitrary_types_allowed = True
        getter_dict = PlanObjectGetter
        orm_mode = True


class PlanOrderGetter(BaseGetterDict):
    """Represents dictionary-like interface to execute data binding with PlanOrder class."""

    def get(self, key: str, default: Any) -> Any:

        if key == "gml_id":
            return self.xpath(constants.XPATH_GML_ID, default)
        if key == "producer_specific_identifier":
            return self.xpath(constants.XPATH_PRODUCER_SPECIFIC_IDENTIFIER, default)
        if key == "xml":
            return self._obj
        return default  # pragma: no cover


class PlanOrder(BaseModel):
    """Represents model definition for PlanOrder class."""

    gml_id: str
    producer_specific_identifier: str
    xml: ET._Element

    class Config:
        arbitrary_types_allowed = True
        getter_dict = PlanOrderGetter
        orm_mode = True


class PlannerGetter(BaseGetterDict):
    """Represents dictionary-like interface to execute data binding with Planner class."""

    def get(self, key: str, default: Any) -> Any:

        if key == "gml_id":
            return self.xpath(constants.XPATH_GML_ID, default)
        if key == "producer_specific_identifier":
            return self.xpath(constants.XPATH_PRODUCER_SPECIFIC_IDENTIFIER, default)
        if key == "xml":
            return self._obj
        return default  # pragma: no cover


class Planner(BaseModel):
    """Represents model definition for Planner class."""

    gml_id: str
    producer_specific_identifier: str
    xml: ET._Element

    class Config:
        arbitrary_types_allowed = True
        getter_dict = PlannerGetter
        orm_mode = True


class SpatialPlanGetter(BaseGetterDict):
    """Represents dictionary-like interface to execute data binding with SpatialPlan class."""

    def get(self, key: str, default: Any) -> Any:

        if key == "boundary":
            geometry = list(self.xpath(constants.XPATH_BOUNDARY, default))[0]
            return shape(pygml.parse(geometry))
        if key == "general_order":
            return self.xpath(constants.XPATH_GENERAL_ORDER, default)
        if key == "gml_id":
            return self.xpath(constants.XPATH_GML_ID, default)
        if key == "planner":
            return self.xpath(constants.XPATH_PLANNER, default)
        if key == "participation_and_evalution_plan":
            return self.xpath(constants.XPATH_PARTICIPATION_AND_EVALUTION_PLAN, default)
        if key == "producer_specific_identifier":
            return self.xpath(constants.XPATH_PRODUCER_SPECIFIC_IDENTIFIER, default)
        if key == "plan_identifier":
            return self.xpath(constants.XPATH_PLAN_IDENTIFIER, default)
        if key == "xml":
            return self._obj
        return default  # pragma: no cover


class SpatialPlan(BaseModel):
    """Represents model definition for SpatialPlan class."""

    boundary: BaseGeometry
    general_order: str
    gml_id: str
    participation_and_evalution_plan: str
    plan_identifier: str
    planner: str
    producer_specific_identifier: str
    xml: ET._Element

    class Config:
        arbitrary_types_allowed = True
        getter_dict = SpatialPlanGetter
        orm_mode = True
