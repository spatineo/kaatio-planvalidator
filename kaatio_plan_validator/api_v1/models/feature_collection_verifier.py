from pydantic import BaseModel

from .. import exceptions
from .land_use_feature_collection import LandUseFeatureCollection
from .participation_and_evaluation_plan import ParticipationAndEvaluationPlan
from .plan_object import PlanObject
from .plan_order import PlanOrder
from .planner import Planner
from .spatial_plan import SpatialPlan


class FeatureCollectionVerifier(BaseModel):

    errors: list[str] = []

    participation_and_evaluation_plans: list[ParticipationAndEvaluationPlan] = []
    plan_objects: list[PlanObject] = []
    plan_orders: list[PlanOrder] = []
    planners: list[Planner] = []
    spatial_plans: list[SpatialPlan] = []

    @classmethod
    def parse_feature_collection(cls, feature_collection: LandUseFeatureCollection):

        return cls(
            participation_and_evaluation_plans=[
                ParticipationAndEvaluationPlan.from_orm(element)
                for element in feature_collection.find_feature_members_by_tag("ParticipationAndEvaluationPlan")
            ],
            plan_objects=[
                PlanObject.from_orm(element)
                for element in feature_collection.find_feature_members_by_tag("PlanObject")
            ],
            plan_orders=[
                PlanOrder.from_orm(element) for element in feature_collection.find_feature_members_by_tag("PlanOrder")
            ],
            planners=[
                Planner.from_orm(element) for element in feature_collection.find_feature_members_by_tag("Planner")
            ],
            spatial_plans=[
                SpatialPlan.from_orm(element)
                for element in feature_collection.find_feature_members_by_tag("SpatialPlan")
            ],
        )

    def has_participation_and_evaluation_plans_with_known_feature_member_references(self) -> None:
        pass

    def has_plan_objects_with_known_feature_member_references(self) -> None:

        spatial_plan_gml_ids = [i.gml_id for i in self.spatial_plans]

        for plan_object in self.plan_objects:
            # Check spatialPlan
            if plan_object.spatial_plan:
                try:
                    assert (
                        plan_object.spatial_plan not in spatial_plan_gml_ids
                    ), f"{plan_object.gml_id} has unknown spatialPlan: {plan_object.spatial_plan}!"
                except AssertionError as err:
                    self.errors.append(str(err))

    def has_plan_orders_with_known_feature_member_references(self) -> None:

        spatial_plan_gml_ids = [i.gml_id for i in self.spatial_plans]

        for plan_order in self.plan_orders:
            # Check spatialPlan
            if plan_order.spatial_plan:
                try:
                    assert (
                        plan_order.gml_id not in spatial_plan_gml_ids
                    ), f"{plan_order.gml_id} has unknown spatialPlan: {plan_order.spatial_plan}!"
                except AssertionError as err:
                    self.errors.append(str(err))

    def has_planners_with_known_feature_member_references(self) -> None:
        pass

    def has_spatial_plans_with_known_feature_member_references(self) -> None:

        participation_and_evaluation_plan_gml_ids = [i.gml_id for i in self.participation_and_evaluation_plans]
        plan_order_gml_ids = [i.gml_id for i in self.plan_orders]
        planner_gml_ids = [i.gml_id for i in self.planners]

        for spatial_plan in self.spatial_plans:
            # Check generalOrder
            if spatial_plan.general_order:
                try:
                    assert (
                        spatial_plan.general_order not in plan_order_gml_ids
                    ), f"{spatial_plan.gml_id} has unknown generalOrder: {spatial_plan.general_order}!"
                except AssertionError as err:
                    self.errors.append(str(err))
            # Check planner
            if spatial_plan.planner:
                try:
                    assert (
                        spatial_plan.planner not in planner_gml_ids
                    ), f"{spatial_plan.gml_id} has unknown planner: {spatial_plan.planner}!"
                except AssertionError as err:
                    self.errors.append(str(err))
            # Check participationAndEvalutionPlan
            if spatial_plan.participation_and_evalution_plan:
                try:
                    assert (
                        spatial_plan.planner not in participation_and_evaluation_plan_gml_ids
                    ), f"{spatial_plan.gml_id} has unknown participationAndEvalutionPlan: {spatial_plan.participation_and_evalution_plan}!"
                except AssertionError as err:
                    self.errors.append(str(err))

    def verify(self) -> bool:

        self.has_participation_and_evaluation_plans_with_known_feature_member_references()
        self.has_plan_objects_with_known_feature_member_references()
        self.has_plan_orders_with_known_feature_member_references()
        self.has_planners_with_known_feature_member_references()
        self.has_spatial_plans_with_known_feature_member_references

        if self.errors:
            raise exceptions.VerifyException(str(self.errors))
