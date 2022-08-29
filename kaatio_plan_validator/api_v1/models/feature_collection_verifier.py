from pydantic import BaseModel

from .. import exceptions
from .participation_and_evaluation_plan import ParticipationAndEvaluationPlan
from .plan_object import PlanObject
from .plan_order import PlanOrder
from .planner import Planner
from .spatial_plan import SpatialPlan


class FeatureCollectionVerifier(BaseModel):

    participation_and_evaluation_plans: list[ParticipationAndEvaluationPlan]
    plan_objects: list[PlanObject]
    plan_orders: list[PlanOrder]
    planners: list[Planner]
    spatial_plans: list[SpatialPlan]

    def has_participation_and_evaluation_plans_with_known_feature_member_references(self):
        pass

    def has_plan_objects_with_known_feature_member_references(self):
        spatial_plan_gml_ids = [i.gml_id for i in self.spatial_plans]
        for plan_object in self.plan_objects:
            # Check spatialPlan
            if plan_object.spatial_plan and plan_object.spatial_plan.removeprefix("#") not in spatial_plan_gml_ids:
                raise exceptions.VerifyException(
                    reason=f"{plan_object.gml_id} has unknown spatialPlan: {plan_object.spatial_plan}!",
                )

    def has_plan_orders_with_known_feature_member_references(self):
        spatial_plan_gml_ids = [i.gml_id for i in self.spatial_plans]
        for plan_order in self.plan_orders:
            # Check spatialPlan
            if plan_order.spatial_plan and plan_order.spatial_plan.removeprefix("#") not in spatial_plan_gml_ids:
                raise exceptions.VerifyException(
                    reason=f"{plan_order.gml_id} has unknown spatialPlan: {plan_order.spatial_plan}!",
                )

    def has_planners_with_known_feature_member_references(self):
        pass

    def has_spatial_plans_with_known_feature_member_references(self):
        participation_and_evaluation_plan_gml_ids = [i.gml_id for i in self.participation_and_evaluation_plans]
        plan_order_gml_ids = [i.gml_id for i in self.plan_orders]
        planner_gml_ids = [i.gml_id for i in self.planners]

        for spatial_plan in self.spatial_plans:
            # Check generalOrder
            if spatial_plan.general_order and spatial_plan.general_order.removeprefix("#") not in plan_order_gml_ids:
                raise exceptions.VerifyException(
                    reason=f"{spatial_plan.gml_id} has unknown generalOrder: {spatial_plan.general_order}!",
                )
            # Check planner
            if spatial_plan.planner and spatial_plan.planner.removeprefix("#") not in planner_gml_ids:
                raise exceptions.VerifyException(
                    reason=f"{spatial_plan.gml_id} has unknown planner: {spatial_plan.planner}!",
                )
            # Check participationAndEvalutionPlan
            if (
                spatial_plan.participation_and_evalution_plan
                and spatial_plan.participation_and_evalution_plan.removeprefix("#")
                not in participation_and_evaluation_plan_gml_ids
            ):
                raise exceptions.VerifyException(
                    reason=f"{spatial_plan.gml_id} has unknown participationAndEvalutionPlan: {spatial_plan.participation_and_evalution_plan}!",
                )

    def has_spatial_plans_with_boundary_contains_plan_object_geometry():
        pass

    def verify(self) -> bool:
        self.has_participation_and_evaluation_plans_with_known_feature_member_references()
        self.has_plan_objects_with_known_feature_member_references()
        self.has_plan_orders_with_known_feature_member_references()
        self.has_planners_with_known_feature_member_references()
        self.has_spatial_plans_with_known_feature_member_references()
        return True
