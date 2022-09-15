import warnings
from typing import Any

import lxml.etree as ET
import xmlschema
from pydantic import BaseModel, validator

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


class LandUseFeatureCollection(BaseModel):
    """Represents model definition of LandUseFeatureCollection."""

    xml: ET._ElementTree

    spatial_plan: SpatialPlan

    pe_plans: list[ParticipationAndEvaluationPlan] = []
    plan_objects: list[PlanObject] = []
    plan_orders: list[PlanOrder] = []
    planners: list[Planner] = []

    class Config:
        """Represents config definition for model."""

        arbitrary_types_allowed = True

    @classmethod
    def from_xml_source(cls, source: Any):
        """Create instance from source XML."""

        def get_feature_members_by_tag(root: ET._Element, tag: str) -> list[ET._Element]:
            """Returns list of elements found with given tag."""
            return [
                feature_member
                for feature_members in list(root)
                for feature_member in list(feature_members)
                if isinstance(feature_member, ET._Element) and feature_member.xpath(constants.XPATH_LOCAL_NAME) == tag
            ]

        try:
            # Parse XML.
            xml: ET._ElementTree = ET.parse(source)
            # Execute XML schema validation.
            xsd.validate(xml)

            root = xml.getroot()

            return cls(
                spatial_plan=[
                    SpatialPlan.from_orm(feature_member_element)
                    for feature_member_element in get_feature_members_by_tag(
                        root=root,
                        tag="SpatialPlan",
                    )
                ][0],
                pe_plans=[
                    ParticipationAndEvaluationPlan.from_orm(feature_member_element)
                    for feature_member_element in get_feature_members_by_tag(
                        root=root,
                        tag="ParticipationAndEvaluationPlan",
                    )
                ],
                plan_objects=[
                    PlanObject.from_orm(feature_member_element)
                    for feature_member_element in get_feature_members_by_tag(
                        root=root,
                        tag="PlanObject",
                    )
                ],
                plan_orders=[
                    PlanOrder.from_orm(feature_member_element)
                    for feature_member_element in get_feature_members_by_tag(
                        root=root,
                        tag="PlanOrder",
                    )
                ],
                planners=[
                    Planner.from_orm(feature_member_element)
                    for feature_member_element in get_feature_members_by_tag(
                        root=root,
                        tag="Planner",
                    )
                ],
                xml=xml,
            )
        except ET.ParseError as err:
            raise exceptions.ParserException(f"Failed to parse XML! Reason: {err}")
        except xmlschema.XMLSchemaException as err:
            raise exceptions.SchemaException(f"Failed to validate XML against schema! Reason: {err}")

    @validator("xml")
    def xml_root_tag_is_verified(cls, xml: ET._ElementTree):
        tag = xml.xpath(constants.XPATH_LOCAL_NAME)
        assert tag == "LandUseFeatureCollection", "XML root element should be LandUseFeatureCollection!"
        return xml

    def to_string(self) -> str:
        """Returns XML in string representation."""
        try:
            xsd.validate(self.xml)
        except xmlschema.XMLSchemaException as err:
            raise exceptions.VerifyException(f"Failed to validate XML against schema! Reason: {err}")

        return ET.tostring(
            self.xml,
            encoding="unicode",
            pretty_print=True,
        )

    def update_ids_and_refs(self):

        spatial_plan_refs = [self.spatial_plan.update_or_create_elements_with_id()]

        pe_plan_refs = [element.update_or_create_elements_with_id() for element in self.pe_plans]
        plan_object_refs = [element.update_or_create_elements_with_id() for element in self.plan_objects]
        plan_orders_refs = [element.update_or_create_elements_with_id() for element in self.plan_orders]
        planner_refs = [element.update_or_create_elements_with_id() for element in self.planners]

        self.spatial_plan.update_feature_member_id_references(
            xpath=constants.XPATH_GENERAL_ORDER,
            refs=plan_orders_refs,
        )
        self.spatial_plan.update_feature_member_id_references(
            xpath=constants.XPATH_PLANNER,
            refs=planner_refs,
        )
        self.spatial_plan.update_feature_member_id_references(
            xpath=constants.XPATH_PARTICIPATION_AND_EVALUTION_PLAN,
            refs=pe_plan_refs,
        )
        self.spatial_plan.update_or_create_storage_time()
        self.spatial_plan.post_validate()

        for pe_plan in self.pe_plans:
            pe_plan.update_or_create_storage_time()
            pe_plan.post_validate()

        for plan_object in self.plan_objects:
            plan_object.update_feature_member_id_references(
                xpath=constants.XPATH_SPATIAL_PLAN,
                refs=spatial_plan_refs,
            )
            plan_object.update_or_create_storage_time()
            plan_object.post_validate()

        for plan_order in self.plan_orders:
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

        for planner in self.planners:
            planner.update_or_create_storage_time()
            planner.post_validate()
