from pathlib import Path

import pytest
from pydantic import ValidationError

from kaatio_plan_validator.api_v1 import exceptions, models


def test_feature_collection_verifier(land_use_feature_collection: models.LandUseFeatureCollection):

    verifier = models.FeatureCollectionVerifier(
        participation_and_evaluation_plans=[
            models.ParticipationAndEvaluationPlan.from_orm(element)
            for element in land_use_feature_collection.find_feature_members_by_tag("ParticipationAndEvaluationPlan")
        ],
        plan_objects=[
            models.PlanObject.from_orm(element)
            for element in land_use_feature_collection.find_feature_members_by_tag("PlanObject")
        ],
        plan_orders=[
            models.PlanOrder.from_orm(element)
            for element in land_use_feature_collection.find_feature_members_by_tag("PlanOrder")
        ],
        planners=[
            models.Planner.from_orm(element)
            for element in land_use_feature_collection.find_feature_members_by_tag("Planner")
        ],
        spatial_plans=[
            models.SpatialPlan.from_orm(element)
            for element in land_use_feature_collection.find_feature_members_by_tag("SpatialPlan")
        ],
    )
    assert verifier.verify()


def test_model_land_use_feature_collection_with_broken_xml(broken_xml: Path):

    with pytest.raises(exceptions.ParserException):
        models.LandUseFeatureCollection.parse_xml(
            source=broken_xml,
        )


def test_model_land_use_feature_collection_with_invalid_xml(invalid_xml: Path):

    with pytest.raises(exceptions.SchemaException):
        models.LandUseFeatureCollection.parse_xml(
            source=invalid_xml,
        )


def test_model_land_use_feature_collection_with_invalid_xml_no_feature_members(invalid_xml_no_feature_members: Path):

    with pytest.raises(ValidationError):
        models.LandUseFeatureCollection.parse_xml(
            skip={"no_xsd_validation": True},
            source=invalid_xml_no_feature_members,
        )


def test_model_land_use_feature_collection_with_valid_xml_1(valid_xml_1: Path):

    model = models.LandUseFeatureCollection.parse_xml(
        source=valid_xml_1,
    )
    assert model
    assert len(model.find_feature_members_by_tag("ParticipationAndEvaluationPlan")) == 1
    assert len(model.find_feature_members_by_tag("PlanObject")) == 1
    assert len(model.find_feature_members_by_tag("PlanOrder")) == 2
    assert len(model.find_feature_members_by_tag("Planner")) == 1
    assert len(model.find_feature_members_by_tag("SpatialPlan")) == 1


def test_model_land_use_feature_collection_with_valid_xml_2(valid_xml_2: Path):

    model = models.LandUseFeatureCollection.parse_xml(
        source=valid_xml_2,
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


def test_model_planner(land_use_feature_collection: models.LandUseFeatureCollection):

    for planner in land_use_feature_collection.find_feature_members_by_tag("Planner"):
        model = models.Planner.from_orm(planner)
        assert model


def test_model_spatial_plan(land_use_feature_collection: models.LandUseFeatureCollection):

    for spatial_plan in land_use_feature_collection.find_feature_members_by_tag("SpatialPlan"):
        model = models.SpatialPlan.from_orm(spatial_plan)
        assert model
