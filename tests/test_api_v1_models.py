from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from kaatio_plan_validator.api_v1 import exceptions, models

if TYPE_CHECKING:
    from pathlib import Path


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
    assert len(model.participation_and_evaluation_plans) == 1
    assert len(model.plan_objects) == 1
    assert len(model.plan_orders) == 2
    assert len(model.planners) == 1
    assert len(model.spatial_plans) == 1


def test_model_participation_and_evaluation_plan(land_use_feature_collection: models.LandUseFeatureCollection):

    for participation_and_evaluation_plan in land_use_feature_collection.participation_and_evaluation_plans:
        assert models.ParticipationAndEvaluationPlan.from_orm(participation_and_evaluation_plan)


def test_model_plan_object(land_use_feature_collection: models.LandUseFeatureCollection):

    for plan_object in land_use_feature_collection.plan_objects:
        assert models.PlanObject.from_orm(plan_object)


def test_model_plan_order(land_use_feature_collection: models.LandUseFeatureCollection):

    for plan_order in land_use_feature_collection.plan_orders:
        assert models.PlanOrder.from_orm(plan_order)


def test_model_planner(land_use_feature_collection: models.LandUseFeatureCollection):

    for planner in land_use_feature_collection.planners:
        assert models.Planner.from_orm(planner)


def test_model_spatial_plan(land_use_feature_collection: models.LandUseFeatureCollection):

    for spatial_plan in land_use_feature_collection.spatial_plans:
        assert models.SpatialPlan.from_orm(spatial_plan)
