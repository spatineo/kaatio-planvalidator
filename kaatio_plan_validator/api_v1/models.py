from __future__ import annotations

from typing import Any

import lxml.etree as ET
import pygml
import xmlschema
from pydantic import BaseModel, validator
from shapely.geometry import shape

from . import constants, exceptions


class DocumentModel(BaseModel):

    doc: ET._ElementTree | ET._Element
    errors: list[str] = []

    class Config:
        arbitrary_types_allowed = True

    def xpath(self, xpath: str) -> Any:

        try:
            return self.doc.xpath(xpath, namespaces=constants.NAMESPACES)[0]
        except IndexError:  # pragma: no cover
            return None


class LandUseFeatureCollection(DocumentModel):
    """"""

    @classmethod
    def parse_xml(cls, source: Any):
        try:
            return cls(
                doc=ET.parse(source),
            )
        except ET.ParseError as err:
            raise exceptions.ParserException(str(err))

    @validator("doc")
    def doc_must_validate_against_xsd(cls, v):
        xsd = xmlschema.XMLSchema(
            constants.SCHEMA_FILES,
            allow="sandbox",
            base_url=str(constants.SCHEMA_DIR),
            defuse="always",
        )
        try:
            xsd.validate(v)
            return v
        except xmlschema.XMLSchemaException as err:
            raise exceptions.ValidatorException(str(err))

    def filter_feature_members_by_tag(self, tag: str):

        return [
            fm
            for fms in list(self.doc.getroot())
            for fm in list(fms)
            if isinstance(fm, ET._Element) and fm.xpath("local-name()") == tag
        ]

    def to_string(self) -> str:
        return ET.tostring(self.doc)

    def validate_feature_members(self) -> list[list[str]]:
        return [item.errors for item in self.plan_orders if not item.validate_doc()]

    @property
    def participation_and_evaluation_plans(self) -> list[ParticipationAndEvaluationPlan]:
        return [
            ParticipationAndEvaluationPlan(
                doc=item,
            )
            for item in self.filter_feature_members_by_tag("ParticipationAndEvaluationPlan")
        ]

    @property
    def plan_objects(self) -> list[PlanObject]:
        return [
            PlanObject(
                doc=item,
            )
            for item in self.filter_feature_members_by_tag("PlanObject")
        ]

    @property
    def plan_orders(self) -> list[PlanOrder]:
        return [
            PlanOrder(
                doc=item,
            )
            for item in self.filter_feature_members_by_tag("PlanOrder")
        ]

    @property
    def planners(self) -> list[Planner]:
        return [
            Planner(
                doc=item,
            )
            for item in self.filter_feature_members_by_tag("Planner")
        ]

    @property
    def spatial_plans(self) -> list[SpatialPlan]:
        return [
            SpatialPlan(
                doc=item,
            )
            for item in self.filter_feature_members_by_tag("SpatialPlan")
        ]


class ParticipationAndEvaluationPlan(DocumentModel):
    """"""

    @property
    def gml_id(self) -> str:
        return self.xpath("./@gml:id")

    @property
    def producer_specific_identifier(self) -> str:
        return self.xpath("lud-core:producerSpecificIdentifier/text()")


class PlanObject(DocumentModel):
    """"""

    @property
    def geometry(self):
        try:
            element = list(self.xpath("splan:geometry"))[0]
            return shape(pygml.parse(element).__geo_interface__)
        except IndexError:  # pragma: no cover
            return None

    @property
    def gml_id(self) -> str:
        return self.xpath("./@gml:id")

    @property
    def producer_specific_identifier(self) -> str:
        return self.xpath("lud-core:producerSpecificIdentifier/text()")


class PlanOrder(DocumentModel):
    """"""

    def validate_doc(self) -> bool:
        try:
            assert self.gml_id, "Required value missing: gml:id"
        except AssertionError as err:
            self.errors.append(err)

        try:
            assert self.producer_specific_identifier, "Required value missing: producerSpecificIdentifier"
        except AssertionError as err:
            self.errors.append(err)

        return bool(not self.errors)

    @property
    def gml_id(self) -> str:
        return self.xpath("./@gml:id")

    @gml_id.setter
    def gml_id(self, value: str) -> None:
        element = self.xpath(".")
        if isinstance(element, ET._Element):
            element.attrib["gml:id"] = value

    @property
    def producer_specific_identifier(self) -> str:
        return self.xpath("lud-core:producerSpecificIdentifier/text()")


class Planner(DocumentModel):
    """"""

    @property
    def gml_id(self) -> str:
        return self.xpath("./@gml:id")

    @property
    def producer_specific_identifier(self) -> str:
        return self.xpath("lud-core:producerSpecificIdentifier/text()")


class SpatialPlan(DocumentModel):
    """"""

    @property
    def gml_id(self) -> str:
        return self.xpath("./@gml:id")

    @property
    def producer_specific_identifier(self) -> str:
        return self.xpath("lud-core:producerSpecificIdentifier/text()")

    @property
    def plan_identifier(self) -> str:
        return self.xpath("splan:planIdentifier/text()")
