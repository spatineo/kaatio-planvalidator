from pathlib import Path

import pytest

from kaatio_plan_validator.api_v1 import exceptions, models


def test_model_land_use_feature_collection_from_xml_source_with_broken_xml(broken_xml: Path):

    with pytest.raises(exceptions.ParserException):
        models.LandUseFeatureCollection.from_xml_source(
            source=broken_xml,
        )


def test_model_land_use_feature_collection_from_xml_source_with_invalid_xml(invalid_xml: Path):

    with pytest.raises(exceptions.SchemaException):
        models.LandUseFeatureCollection.from_xml_source(
            source=invalid_xml,
        )


def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_1(valid_xml_1: Path, valid_xml_1_gen: Path):

    model = models.LandUseFeatureCollection.from_xml_source(
        source=valid_xml_1,
        skip_schema_validation=True,
    )
    assert model
    model.update_ids_and_refs()

    with open(valid_xml_1_gen, "w") as output:
        output.write(model.to_string())


@pytest.mark.skip(reason="Debug stuff")
def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_1_gen(
    valid_xml_1_gen: Path,
    valid_xml_1_gen_result: Path,
):

    if valid_xml_1_gen.exists():

        model = models.LandUseFeatureCollection.from_xml_source(
            source=valid_xml_1_gen,
        )
        assert model
        model.update_ids_and_refs()

    with open(valid_xml_1_gen_result, "w") as output:
        output.write(model.to_string())


def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_2(valid_xml_2: Path, valid_xml_2_gen: Path):

    model = models.LandUseFeatureCollection.from_xml_source(
        source=valid_xml_2,
        skip_schema_validation=True,
    )
    assert model
    model.update_ids_and_refs()

    with open(valid_xml_2_gen, "w") as output:
        output.write(model.to_string())


@pytest.mark.skip(reason="Debug stuff")
def test_model_land_use_feature_collection_from_xml_source_with_valid_xml_2_gen(
    valid_xml_2_gen: Path,
    valid_xml_2_gen_result: Path,
):

    if valid_xml_2_gen.exists():

        model = models.LandUseFeatureCollection.from_xml_source(
            source=valid_xml_2_gen,
        )
        assert model
        model.update_ids_and_refs()

    with open(valid_xml_2_gen_result, "w") as output:
        output.write(model.to_string())
