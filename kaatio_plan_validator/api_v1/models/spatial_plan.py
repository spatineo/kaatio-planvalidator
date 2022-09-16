from osgeo import ogr
from pydantic import Field, validator

from .feature_member import FeatureMember


class SpatialPlan(FeatureMember):
    """Represents model definition of SpatialPlan."""

    ref_errors: list = Field(default_factory=list, alias="splan:SpatialPlan")

    plan_identifier: str = Field(alias="splan:SpatialPlan/splan:planIdentifier")
    boundary: ogr.Geometry | None = Field(alias="splan:SpatialPlan/lud-core:boundary")

    @validator("boundary")
    def boundary_is_valid(cls, boundary: ogr.Geometry):
        assert boundary.IsValid(), "boundary is not valid"
        return boundary
