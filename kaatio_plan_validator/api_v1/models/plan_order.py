from typing import Optional

from . import common


class PlanOrder(common.XmlOrmModel):
    """Represents model definition for PlanOrder class."""

    spatial_plan: str
    target: Optional[str]
