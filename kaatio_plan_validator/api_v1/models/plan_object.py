from pydantic import Field, validator
from shapely.ops import BaseGeometry

from .feature_member import FeatureMember


class PlanObject(FeatureMember):
    """Represents model definition of PlanObject."""

    geometry: BaseGeometry = Field(alias="splan:PlanObject/splan:geometry")

    @validator("geometry")
    def geometry_is_valid(cls, geometry: BaseGeometry):
        assert geometry.is_valid, "geometry is not valid"
        return geometry
