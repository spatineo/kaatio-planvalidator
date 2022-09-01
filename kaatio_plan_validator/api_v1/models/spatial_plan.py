from typing import Optional

from pydantic import Field, validator
from shapely.ops import BaseGeometry

from .feature_member import FeatureMember


class SpatialPlan(FeatureMember):
    """Represents model definition of SpatialPlan."""

    plan_identifier: str = Field(alias="splan:SpatialPlan/splan:planIdentifier")
    boundary: Optional[BaseGeometry] = Field(alias="splan:SpatialPlan/lud-core:boundary")

    @validator("boundary")
    def boundary_is_valid(cls, boundary: BaseGeometry):
        assert boundary.is_valid, "boundary is not valid"
        return boundary
