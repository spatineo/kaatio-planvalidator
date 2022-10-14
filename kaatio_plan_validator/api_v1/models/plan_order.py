from pydantic import Field

from .feature_member import FeatureMember


class PlanOrder(FeatureMember):
    """Represents model definition of PlanOrder."""

    ref_errors: list = Field(default_factory=list, alias="splan:PlanOrder")
