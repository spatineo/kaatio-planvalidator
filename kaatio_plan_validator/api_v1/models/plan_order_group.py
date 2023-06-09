from pydantic import Field

from .feature_member import FeatureMember


class PlanOrderGroup(FeatureMember):
    """Represents model definition of PlanOrderGroup."""

    ref_errors: list = Field(default_factory=list, alias="splan:PlanOrderGroup")
