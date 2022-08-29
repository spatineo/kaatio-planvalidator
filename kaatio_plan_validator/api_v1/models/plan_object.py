from pydantic import validator
from shapely.ops import BaseGeometry

from . import common


class PlanObject(common.XmlOrmModel):
    """Represents model definition for PlanObject class."""

    geometry: BaseGeometry
    spatial_plan: str

    @validator("geometry")
    def geometry_is_valid(cls, geometry: BaseGeometry):
        assert geometry.is_valid, "Plan object has invalid geometry!"
        return geometry
