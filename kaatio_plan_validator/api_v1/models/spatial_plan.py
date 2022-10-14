from osgeo import ogr
from pydantic import Field, validator

from kaatio_plan_validator.api_v1.ogc import gdal_err

from .feature_member import FeatureMember


class SpatialPlan(FeatureMember):
    """Represents model definition of SpatialPlan."""

    ref_errors: list = Field(default_factory=list, alias="splan:SpatialPlan")

    plan_identifier: str = Field(alias="splan:SpatialPlan/splan:planIdentifier")
    boundary: ogr.Geometry | None = Field(alias="splan:SpatialPlan/lud-core:boundary")

    @validator("boundary", always=True)
    def boundary_is_valid(cls, boundary: ogr.Geometry | None):
        if boundary:
            try:
                assert boundary.IsValid(), "boundary is not valid"
            except AssertionError:
                if gdal_err.err_msg != "SFCGAL support not enabled.":
                    raise
        return boundary
