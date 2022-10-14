from pydantic import Field

from .feature_member import FeatureMember


class ParticipationAndEvaluationPlan(FeatureMember):
    """Represents model definition of ParticipationAndEvaluationPlan."""

    ref_errors: list = Field(default_factory=list, alias="splan:ParticipationAndEvaluationPlan")
