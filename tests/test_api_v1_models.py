from __future__ import annotations

from typing import TYPE_CHECKING

from kaatio_plan_validator.api_v1 import models

if TYPE_CHECKING:
    from pathlib import Path


def test_model_land_use_feature_collection(valid_xml: Path):

    model = models.LandUseFeatureCollection.parse_xml(
        source=valid_xml,
    )
    print(model.dict())

    assert len(model.participation_and_evaluation_plans) == 1
    assert len(model.plan_objects) == 1
    assert len(model.plan_orders) == 2
    assert len(model.planners) == 1
    assert len(model.spatial_plans) == 1

    for item in model.participation_and_evaluation_plans:
        assert item.gml_id
        assert item.producer_specific_identifier

    for item in model.plan_objects:
        assert item.geometry
        assert item.gml_id
        assert item.producer_specific_identifier

    for item in model.plan_orders:
        assert item.validate_doc()

    for item in model.planners:
        assert item.gml_id
        assert item.producer_specific_identifier

    for item in model.spatial_plans:
        assert item.gml_id
        assert item.producer_specific_identifier
        assert item.plan_identifier
