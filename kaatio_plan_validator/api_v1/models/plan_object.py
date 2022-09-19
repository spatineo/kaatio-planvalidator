from osgeo import ogr
from pydantic import Field, validator

from .feature_member import FeatureMember


class PlanObject(FeatureMember):
    """Represents model definition of PlanObject."""

    ref_errors: list = Field(default_factory=list, alias="splan:PlanObject")
    geometry: ogr.Geometry | None = Field(alias="splan:PlanObject/splan:geometry")

    @validator("geometry")
    def geometry_is_valid(cls, geometry: ogr.Geometry):
        assert geometry.IsValid(), "geometry is not valid"
        return geometry
