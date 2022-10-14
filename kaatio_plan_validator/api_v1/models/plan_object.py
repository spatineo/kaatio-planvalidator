from osgeo import ogr
from pydantic import Field, validator

from kaatio_plan_validator.api_v1.ogc import gdal_err

from .feature_member import FeatureMember


class PlanObject(FeatureMember):
    """Represents model definition of PlanObject."""

    ref_errors: list = Field(default_factory=list, alias="splan:PlanObject")
    geometry: ogr.Geometry | None = Field(alias="splan:PlanObject/splan:geometry")

    @validator("geometry", always=True)
    def geometry_is_valid(cls, geometry: ogr.Geometry | None):
        if geometry:
            try:
                assert geometry.IsValid(), "geometry is not valid"
            except AssertionError:
                if gdal_err.err_msg != "SFCGAL support not enabled.":
                    raise

        return geometry
