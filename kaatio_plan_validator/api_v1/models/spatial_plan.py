from shapely.ops import BaseGeometry

from . import common


class SpatialPlan(common.XmlOrmModel):
    """Represents model definition for SpatialPlan class."""

    boundary: BaseGeometry
    general_order: str
    participation_and_evalution_plan: str
    plan_identifier: str
    planner: str
