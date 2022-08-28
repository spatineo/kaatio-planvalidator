from shapely.ops import BaseGeometry

from . import common


class PlanObject(common.XmlOrmModel):
    """Represents model definition for PlanObject class."""

    geometry: BaseGeometry
    spatial_plan: str
