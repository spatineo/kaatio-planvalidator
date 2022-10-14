from pydantic import Field

from .feature_member import FeatureMember


class Planner(FeatureMember):
    """Represents model definition of Planner."""
    ref_errors: list = Field(default_factory=list, alias="splan:Planner")
