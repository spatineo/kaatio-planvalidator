import warnings
from typing import Any

import lxml.etree as ET
import xmlschema
from pydantic import BaseModel, Field, PrivateAttr, validator
from pydantic.dataclasses import dataclass

from .. import constants, exceptions
from .participation_and_evaluation_plan import ParticipationAndEvaluationPlan
from .plan_object import PlanObject
from .plan_order import PlanOrder
from .planner import Planner
from .spatial_plan import SpatialPlan

warnings.simplefilter(action="ignore", category=xmlschema.XMLSchemaImportWarning)

xsd = xmlschema.XMLSchema(
    constants.SCHEMA_FILES,
    allow="sandbox",
    base_url=str(constants.SCHEMA_DIR),
    defuse="always",
)


@dataclass
class LandUseFeatureCollectionMembers:
    """Helper dataclass for feature member instances."""

    spatial_plan: SpatialPlan
    pe_plans: list[ParticipationAndEvaluationPlan]
    plan_objects: list[PlanObject]
    plan_orders: list[PlanOrder]
    planners: list[Planner]


class LandUseFeatureCollection(BaseModel):
    """Represents model definition of LandUseFeatureCollection."""

    xml: ET._ElementTree = Field(alias="lud-core:LandUseFeatureCollection")

    _feature_members: LandUseFeatureCollectionMembers = PrivateAttr(default=None)

    class Config:
        """Represents config definition for model."""

        allow_population_by_field_name = True
        arbitrary_types_allowed = True

    @classmethod
    def from_xml_source(cls, source: Any):
        """Create instance from source XML."""

        try:
            # Parse XML.
            xml: ET._ElementTree = ET.parse(source)
            # Execute XML schema validation.
            xsd.validate(xml)

            return cls(
                xml=xml,
            )
        except ET.ParseError as err:  # pragma: no cover
            raise exceptions.ParserException(f"Failed to parse XML! Reason: {err}")
        except xmlschema.XMLSchemaException as err:  # pragma: no cover
            raise exceptions.SchemaException(f"Failed to validate XML against schema! Reason: {err}")

    @staticmethod
    def find_feature_members_by_tag(xml: ET._ElementTree, tag: str) -> list[ET._Element]:
        return [
            feature_member
            for feature_members in list(xml.getroot())
            for feature_member in list(feature_members)
            if isinstance(feature_member, ET._Element) and feature_member.xpath(constants.XPATH_LOCAL_NAME) == tag
        ]

    @validator("xml")
    def xml_root_tag_is_verified(cls, xml: ET._ElementTree):
        tag = xml.xpath(constants.XPATH_LOCAL_NAME)
        assert tag == "LandUseFeatureCollection", "XML root element should be LandUseFeatureCollection!"
        return xml

    @validator("xml")
    def feature_member_spatial_plan_should_be_present(cls, xml: ET._ElementTree):
        spatial_plans = cls.find_feature_members_by_tag(
            xml=xml,
            tag="SpatialPlan",
        )
        assert len(spatial_plans) == 1, "missing splan:SpatialPlan."
        return xml

    def _process_feature_members(self, feature_members: LandUseFeatureCollectionMembers):
        """Represents business logic for processing collected feature_members."""

        spatial_plan_refs = [feature_members.spatial_plan.update_or_create_elements_with_id()]
        pe_plan_refs = [instance.update_or_create_elements_with_id() for instance in feature_members.pe_plans]
        plan_object_refs = [instance.update_or_create_elements_with_id() for instance in feature_members.plan_objects]
        plan_orders_refs = [instance.update_or_create_elements_with_id() for instance in feature_members.plan_orders]
        planner_refs = [instance.update_or_create_elements_with_id() for instance in feature_members.planners]

        feature_members.spatial_plan.update_feature_member_id_references(
            xpath=constants.XPATH_GENERAL_ORDER,
            refs=plan_orders_refs,
        )
        feature_members.spatial_plan.update_feature_member_id_references(
            xpath=constants.XPATH_PLANNER,
            refs=planner_refs,
        )
        feature_members.spatial_plan.update_feature_member_id_references(
            xpath=constants.XPATH_PARTICIPATION_AND_EVALUTION_PLAN,
            refs=pe_plan_refs,
        )
        feature_members.spatial_plan.update_or_create_storage_time()
        feature_members.spatial_plan.post_validate()

        for pe_plan in feature_members.pe_plans:
            pe_plan.update_or_create_storage_time()
            pe_plan.post_validate()

        for plan_object in feature_members.plan_objects:
            plan_object.update_feature_member_id_references(
                xpath=constants.XPATH_SPATIAL_PLAN,
                refs=spatial_plan_refs,
            )
            plan_object.update_or_create_storage_time()
            plan_object.post_validate()

        for plan_order in feature_members.plan_orders:
            plan_order.update_feature_member_id_references(
                xpath=constants.XPATH_SPATIAL_PLAN,
                refs=spatial_plan_refs,
            )
            plan_order.update_feature_member_id_references(
                xpath=constants.XPATH_TARGET,
                refs=plan_object_refs,
            )
            plan_order.update_or_create_storage_time()
            plan_order.post_validate()

        for planner in feature_members.planners:
            planner.update_or_create_storage_time()
            planner.post_validate()

    def create_feature_members(self) -> LandUseFeatureCollectionMembers:
        """Creates feature member instances into dataclass for processing."""

        if not self._feature_members:
            self._feature_members = LandUseFeatureCollectionMembers(
                spatial_plan=SpatialPlan.from_orm(
                    self.find_feature_members_by_tag(
                        xml=self.xml,
                        tag="SpatialPlan",
                    )[0]
                ),
                pe_plans=[
                    ParticipationAndEvaluationPlan.from_orm(element)
                    for element in self.find_feature_members_by_tag(
                        xml=self.xml,
                        tag="ParticipationAndEvaluationPlan",
                    )
                ],
                plan_objects=[
                    PlanObject.from_orm(element)
                    for element in self.find_feature_members_by_tag(
                        xml=self.xml,
                        tag="PlanObject",
                    )
                ],
                plan_orders=[
                    PlanOrder.from_orm(element)
                    for element in self.find_feature_members_by_tag(
                        xml=self.xml,
                        tag="PlanOrder",
                    )
                ],
                planners=[
                    Planner.from_orm(element)
                    for element in self.find_feature_members_by_tag(
                        xml=self.xml,
                        tag="Planner",
                    )
                ],
            )
        return self._feature_members

    def process_feature_members(self) -> LandUseFeatureCollectionMembers:
        """Executes feature member processing."""

        feature_members = self.create_feature_members()

        self._process_feature_members(feature_members)

        return feature_members

    def to_string(self) -> str:
        """Returns XML in string representation."""
        try:
            xsd.validate(self.xml)
        except xmlschema.XMLSchemaException as err:  # pragma: no cover
            raise exceptions.VerifyException(f"Failed to validate XML against schema! Reason: {err}")

        return ET.tostring(
            self.xml,
            encoding="unicode",
            pretty_print=True,
        )
