from kaatio_plan_validator.api_v1 import models, verifiers


def test_feature_collection_verifier(land_use_feature_collection: models.LandUseFeatureCollection):

    verifier = verifiers.FeatureCollectionVerifier.parse_feature_collection(
        feature_collection=land_use_feature_collection,
    )
    assert verifier
    assert verifier.has_participation_and_evaluation_plans_with_known_feature_member_references() == []
    assert verifier.has_plan_objects_with_known_feature_member_references() == []
    assert verifier.has_plan_orders_with_known_feature_member_references() == []
    assert verifier.has_planners_with_known_feature_member_references() == []
    assert verifier.has_spatial_plans_with_known_feature_member_references() == []
