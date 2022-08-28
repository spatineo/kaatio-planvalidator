from pathlib import Path

import pytest

from kaatio_plan_validator.api_v1 import exceptions, models


def test_feature_collection_verifier(land_use_feature_collection: models.LandUseFeatureCollection):

    verifier = models.FeatureCollectionVerifier.parse_feature_collection(
        feature_collection=land_use_feature_collection,
    )
    assert verifier
    assert verifier.has_participation_and_evaluation_plans_with_known_feature_member_references() == []
    assert verifier.has_plan_objects_with_known_feature_member_references() == []
    assert verifier.has_plan_orders_with_known_feature_member_references() == []
    assert verifier.has_planners_with_known_feature_member_references() == []
    assert verifier.has_spatial_plans_with_known_feature_member_references() == []


def test_model_land_use_feature_collection_with_broken_xml(broken_xml: Path):

    with pytest.raises(exceptions.ParserException):
        models.LandUseFeatureCollection.parse_xml(
            source=broken_xml,
        )


def test_model_land_use_feature_collection_with_invalid_xml(invalid_xml: Path):

    with pytest.raises(exceptions.ValidatorException):
        models.LandUseFeatureCollection.parse_xml(
            source=invalid_xml,
        )


def test_model_land_use_feature_collection_with_invalid_xml_no_feature_members(invalid_xml_no_feature_members: Path):

    with pytest.raises(exceptions.ValidatorException):
        models.LandUseFeatureCollection.parse_xml(
            source=invalid_xml_no_feature_members,
        )


def test_model_land_use_feature_collection_with_valid_xml(valid_xml: Path):

    model = models.LandUseFeatureCollection.parse_xml(
        source=valid_xml,
    )
    assert model
    assert len(model.find_feature_members_by_tag("ParticipationAndEvaluationPlan")) == 1
    assert len(model.find_feature_members_by_tag("PlanObject")) == 1
    assert len(model.find_feature_members_by_tag("PlanOrder")) == 2
    assert len(model.find_feature_members_by_tag("Planner")) == 1
    assert len(model.find_feature_members_by_tag("SpatialPlan")) == 1


def test_model_participation_and_evaluation_plan(land_use_feature_collection: models.LandUseFeatureCollection):

    for participation_and_evaluation_plan in land_use_feature_collection.find_feature_members_by_tag(
        "ParticipationAndEvaluationPlan"
    ):
        model = models.ParticipationAndEvaluationPlan.from_orm(participation_and_evaluation_plan)
        assert model


def test_model_plan_object(land_use_feature_collection: models.LandUseFeatureCollection):

    for plan_object in land_use_feature_collection.find_feature_members_by_tag("PlanObject"):
        model = models.PlanObject.from_orm(plan_object)
        assert model


def test_model_plan_order(land_use_feature_collection: models.LandUseFeatureCollection):

    for plan_order in land_use_feature_collection.find_feature_members_by_tag("PlanOrder"):
        model = models.PlanOrder.from_orm(plan_order)
        assert model

    print(land_use_feature_collection.to_string())


def test_model_planner(land_use_feature_collection: models.LandUseFeatureCollection):

    for planner in land_use_feature_collection.find_feature_members_by_tag("Planner"):
        model = models.Planner.from_orm(planner)
        assert model


def test_model_spatial_plan(land_use_feature_collection: models.LandUseFeatureCollection):

    for spatial_plan in land_use_feature_collection.find_feature_members_by_tag("SpatialPlan"):
        model = models.SpatialPlan.from_orm(spatial_plan)
        assert model
