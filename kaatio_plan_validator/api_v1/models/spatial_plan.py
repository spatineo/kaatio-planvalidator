from pydantic import validator
from shapely.ops import BaseGeometry

from . import common


class SpatialPlan(common.XmlOrmModel):
    """Represents model definition for SpatialPlan class."""

    boundary: BaseGeometry
    general_order: str
    participation_and_evalution_plan: str
    plan_identifier: str
    planner: str

    @validator("boundary")
    def boundary_is_valid(cls, boundary: BaseGeometry):
        assert boundary.is_valid, "Spatial plan has invalid boundary!"
        return boundary
