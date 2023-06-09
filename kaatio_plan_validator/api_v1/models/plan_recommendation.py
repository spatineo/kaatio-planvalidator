from pydantic import Field

from .feature_member import FeatureMember


class PlanRecommendation(FeatureMember):
    """Represents model definition of PlanRecommendation."""

    ref_errors: list = Field(default_factory=list, alias="splan:PlanRecommendation")
